---
topic: "Infrastructure & Scheduling"
difficulty: Hard
problem: "ChatGPT"
---
# Design ChatGPT (LLM Chat Service) – Solution

**Topic:** Infrastructure & Scheduling · **Difficulty:** Hard · **Question:** ChatGPT - Question

## 1. Requirements

**Functional**
- Send a message in a conversation and receive the model's reply **streamed token by token**
- Create / list / rename / delete conversations; reload history; continue an old conversation
- Stop generation mid-stream; regenerate a reply
- Per-tier limits (messages per window, token budgets, model access)

**Non-functional**
- TTFT < 1-2 s at p95; steady streaming (20-50 tokens/s per user)
- High availability of the chat path; graceful degradation under GPU saturation
- Durable history: a completed reply is never lost
- Cost efficiency: GPU utilisation is the key metric; limits must reflect token cost, not request count
- Safety: input and output moderation

**Out of scope:** model training, retrieval / tools / plugins, image and voice, billing details.

## 2. Back-of-envelope

- 500M messages/day ≈ 6K/s avg, ~20K/s peak. Output ≈ 500 tokens → **~10M output tokens/s at peak** across the fleet. Prefill (~3K tokens in) is extra, but processed in parallel and much faster per token.
- Decode throughput per GPU for a large model with batching: assume ~1-3K tokens/s per GPU (aggregated over a batch of 32-128 sequences). 10M tok/s ÷ ~2K ≈ **~5K GPUs** at peak (order of magnitude; model-parallel replicas span 4-8 GPUs, so ~600-1,200 replicas). Quantisation, speculative decoding and smaller models for the free tier reduce it.
- Concurrency: 20K req/s × ~15 s per answer ≈ **300K open streams** at peak. SSE connections are cheap (a few KB each), so ~300K streams fit on ~30-50 chat servers.
- Storage: a turn ≈ 2-4 KB of text. 500M/day × 3 KB ≈ 1.5 TB/day ≈ 550 TB/yr: a horizontally scaled wide-column store, with cold history on cheaper tiers.

## 3. Core entities and API

Entities: `User`, `Conversation { convId, userId, title, updatedAt }`, `Message { convId, msgId (time-ordered), role, content, model, tokensIn, tokensOut, createdAt }`.

```
POST   /conversations                     -> { convId }
POST   /conversations/{id}/messages       { content, model } -> text/event-stream (SSE: token deltas, then [done])
DELETE /conversations/{id}/generation     stop (also implied by client disconnect)
GET    /conversations?cursor=             list (recent first)
GET    /conversations/{id}/messages?cursor=
```

## 4. High-level design

!ChatGPT - Diagram.excalidraw

1. Client posts a message. The gateway authenticates, then checks **per-user limits in Redis** (messages and token budget, concurrent generations).
2. The Chat Service loads recent history from the conversation store, builds the prompt (system prompt + truncated or summarised history + new message), runs input moderation, and sends it to the **Inference Router**.
3. The router places the request in a **priority queue** and dispatches it to a GPU replica that streams tokens back through the Chat Service to the client over SSE.
4. When generation ends (or is stopped), the full assistant message is published to Kafka, then persisted to the conversation store along with token usage for metering.

## 5. Deep dives

### 5.1 Streaming transport

| Option | Pros | Cons |
|---|---|---|
| **SSE over HTTP/2** | One-directional (what we need), plain HTTP, proxies / auth / retries work, auto-reconnect | No client-to-server on the same channel (use a separate stop call) |
| WebSocket | Bidirectional, low overhead | Sticky stateful connections, harder to load balance and authenticate, overkill |
| Long polling | Works anywhere | High per-token overhead and latency |

Use SSE; send tokens in small chunks (every 1-3 tokens or ~50 ms flush). Disable proxy buffering. Chat servers are stateless apart from open streams: draining on deploy means finishing in-flight streams. **If the client disconnects, cancel the generation upstream** to free the GPU slot immediately.

### 5.2 Conversation storage

Access is by `convId` (read the last N messages, append) and by `userId` (list conversations, recent first). No joins, huge volume: **Cassandra / DynamoDB**.
- `messages`: partition key `convId`, clustering key `msgId` (time-ordered, e.g. ULID). Append is a single-partition write, and reading the last 20 messages is one range query.
- `conversations_by_user`: partition `userId`, clustering `updatedAt DESC` for the sidebar.
- Search over history: asynchronously index into **Elasticsearch / OpenSearch** off the Kafka stream (nice to have, not on the critical path).
- Writing the user message before inference and the assistant message after the stream finishes keeps the hot path short. If the stream dies, store the partial text flagged `incomplete` so the user can retry or continue.
- Cache the active conversation's recent history in Redis (TTL ~10 min) to avoid hitting the DB on every turn.
- Context window: history must fit the model's limit. Strategy: keep the system prompt + last N turns verbatim, summarise or drop older turns, and count tokens with the real tokenizer before sending.

### 5.3 GPU inference: batching, queueing and routing

!ChatGPT - Deep Dive Diagram.excalidraw

- Generation has two phases: **prefill** (process the whole prompt, compute-bound, parallel) and **decode** (one token at a time, memory-bandwidth-bound). One request alone wastes the GPU in decode.
- **Continuous (in-flight) batching** (vLLM, TensorRT-LLM, TGI): the replica adds new requests to the running batch at each decode step and removes finished ones, rather than waiting for a whole batch. This raises throughput several times over static batching.
- **KV cache** memory (per-sequence attention state) caps how many sequences fit per GPU. Paged KV-cache management avoids fragmentation, and **prefix caching** reuses the KV of a shared system prompt or a conversation's earlier turns.
- **Router:** picks the replica with the lowest load (queue length, free KV memory) and prefers a replica that already holds the conversation's prefix (consistent hashing on `convId` with a load cap). Long prefills can be isolated onto separate "prefill" replicas (disaggregated serving) so they do not stall decodes.
- **Admission control:** per-tier queues (paid ahead of free, interactive ahead of batch/API). Each request carries its prompt token count; the router limits queue depth and **estimated wait**. Beyond that, reject quickly rather than hold a user for 60 s.
- Autoscale replicas on queue depth, TTFT and GPU utilisation. Model loading takes minutes (tens of GB of weights from an object store, cached on local NVMe), so keep **warm headroom** and scale ahead of the daily curve.

### 5.4 Rate limiting and quotas by cost

- Requests vary 100x in cost, so limit on **tokens**, not only requests. Redis buckets per user: messages per 3 hours (free), tokens per minute, and **max concurrent generations** (e.g. 1-2).
- Reserve estimated tokens (input + max output) at admission, then **refund the difference** when the real count is known. Usage events go through Kafka to the billing / analytics pipeline.
- Details of the bucket mechanics: see Rate Limiter - Solution.

### 5.5 Overload and failure modes

- **Saturated GPU pool:** shed in order: (1) queue with a visible position / wait estimate within a bound, (2) route free users to a smaller / distilled model, (3) cap max output tokens, (4) return 429 / 503 with `Retry-After`. Never let queues grow unbounded; stale requests (client already gone) must be dropped.
- **Replica dies mid-stream:** the Chat Service detects the broken stream. Either fail with a retry button (simple), or transparently re-issue the prompt plus the text generated so far as a prefix (resume). Idempotency key per message avoids double-charging.
- **Chat server dies:** SSE reconnect with `Last-Event-ID` can re-attach if tokens are buffered briefly in Redis; otherwise the client reloads history and the partial answer.
- **Moderation:** a fast classifier on input and a streaming classifier on output; if the output trips, stop the stream and replace with a refusal. It must run in parallel and add little TTFT.
- **Multi-region:** deploy GPU capacity per region, route the user to the nearest region with spare capacity; conversation store replicated globally (eventual consistency is fine since one user writes one conversation).

## 6. What interviewers look for

- **Junior:** client, API, DB for messages, calls a model service; knows streaming is needed.
- **Mid:** SSE streaming, schema by `convId`, queue in front of inference, rate limits, context-window truncation.
- **Senior:** GPU cost model (tokens/s per GPU, batching, KV cache), continuous batching and prefix caching, tiered admission and shedding, token-based quotas with refunds, stream failure and resume, cancel on disconnect, warm capacity planning.

## 7. Common pitfalls

- Request/response without streaming, so users stare at a spinner for 15 s
- Treating the GPU like a stateless web server: no queue, no admission control, no batching
- Rate limiting by request count only
- Letting generation continue after the client left
- Unbounded context growth in the prompt
- Holding the DB write on the critical path before the first token
- Ignoring model load time when autoscaling
