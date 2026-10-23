---
topic: "Infrastructure & Scheduling"
difficulty: Hard
problem: "ChatGPT"
---
# Design ChatGPT (LLM Chat Service)

**Topic:** Infrastructure & Scheduling · **Difficulty:** Hard · **Answer:** ChatGPT - Solution

## Prompt

Design a chat product backed by a large language model. Users hold multi-turn conversations, see the answer appear token by token, and can come back later to continue or search old conversations. Inference runs on a limited, expensive pool of GPUs. Design the end-to-end system, including how requests are queued, limited and streamed.

## Requirements to pin down (ask the interviewer)

- Free vs paid tiers? Different models, priorities, and quotas per tier?
- Do we only support text, or also files / images / tools? (Assume text, plus the ability to stop a generation.)
- Do users need conversation history, search, sharing, deleting?
- How is cost controlled: per-user message caps, token budgets, concurrency limits?
- Latency targets: time to first token, and tokens per second after that?

## Scale hints

- ~50M daily active users, ~10 messages each: ~500M messages/day (~6K/s avg, ~20K/s peak)
- Average response ~500 output tokens, prompt with history ~2-4K tokens
- Time to first token (TTFT) < 1-2 s; stream at roughly reading speed or faster (20-50 tokens/s per user)
- GPUs are the scarce resource; the rest of the stack is comparatively cheap

## Think about before opening the answer

1. Why is streaming essential, and which protocol would you use (SSE, WebSocket, long polling)?
2. How do you store conversations, and what is the access pattern?
3. How do you queue and schedule work on GPUs, and what does batching change?
4. How do you rate limit when requests vary hugely in cost (tokens, not calls)?
5. What happens when the GPU pool is saturated, or a replica dies in the middle of a stream?

## Self-check

- [ ] I can estimate GPU count from tokens per second per GPU
- [ ] I can explain prefill vs decode and why continuous batching matters
- [ ] I can design the chat history schema and the context-window handling
- [ ] I can describe overload behaviour: queue, shed, degrade
