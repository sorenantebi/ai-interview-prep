---
topic: "Messaging & Real-time"
difficulty: Medium
problem: "Notification System"
---
# Design a Notification System – Solution

**Topic:** Messaging & Real-time · **Difficulty:** Medium · **Question:** Notification System - Question

## 1. Requirements

**Functional**
- Internal services submit a notification request (user or audience, template, data, priority)
- Deliver via push (APNs/FCM), email and SMS (in-app as an extension)
- Respect user preferences (channel opt-in/out, quiet hours) and render localised templates
- Support scheduled and bulk sends; track delivery status

**Non-functional**
- Producers are decoupled: submitting is fast and never blocked by a slow provider
- **At-least-once delivery with de-duplication**, so users do not get repeated messages
- High priority (OTP, security) within seconds, even during a marketing blast
- Scalable bursts (1M+ in minutes), resilient to provider outages, auditable

**Out of scope:** the content authoring UI, campaign segmentation, A/B testing.

## 2. Back-of-envelope

- 10M/day ≈ 115/s average, but a burst of 1M in 5 min ≈ **3.3K/s**. Design for ~10K/s sustained so the queue absorbs peaks.
- Fan-out: one event may target several channels (×2-3), so ~30K channel sends/s at peak.
- Provider limits: FCM/APNs tolerate high concurrency over HTTP/2; SES and SMS gateways have per-account rate limits (tens to hundreds per second), so **throttling is part of the design**.
- Log: 10M/day × ~500 B ≈ 5 GB/day, 30-90 days retention is small.

## 3. Core entities and API

Entities: `Notification { notifId, userId, type, channels[], payload, priority, idempotencyKey, status }`, `UserPref { userId, channel, enabled, quietHours, locale }`, `DeviceToken { userId, platform, token }`, `Template { templateId, locale, body }`.

```
POST /v1/notifications  { idempotencyKey, userId | audienceId, templateId, data, priority, sendAt? }
                        -> 202 Accepted { notifId }
GET  /v1/notifications/{notifId}          -> status per channel
PUT  /v1/users/{id}/preferences           -> opt-in/out, quiet hours
POST /v1/devices                          -> register push token
```

`202 Accepted` is deliberate: submission is asynchronous.

## 4. High-level design

!Notification System - Diagram.excalidraw

1. Producers call the **Notification API**. It authenticates, validates, checks the **idempotency key** in Redis (`SETNX` with TTL), reads **preferences/templates** (cached Postgres), and decides which channels apply.
2. It writes one message per channel to **Kafka**, in separate topics by channel and priority (`push.high`, `push.low`, `email.high`, `email.bulk`, ...).
3. Each channel has its own **worker pool** (autoscaled on consumer lag). A worker renders the template, calls the provider, records the status and retries on failure.
4. Failures after N attempts go to a **retry / dead-letter queue** for inspection and replay.

## 5. Deep dives

### 5.1 Why a queue, and how to split it

- Without a queue, a slow SMS provider would back up all producers; with one, producers get `202` in milliseconds and consumers drain at the provider's pace.
- Kafka (or SQS/RabbitMQ at smaller scale). Kafka gives replay and high throughput; SQS gives per-message visibility timeouts and DLQs out of the box.
- **Separate topics per channel *and* per priority.** If OTPs share a queue with a 1M-message newsletter, they wait behind it (head-of-line blocking). Dedicated high-priority topics with reserved worker capacity protect latency; bulk workers are throttled to leave provider quota for them.

### 5.2 Reliability: retries, idempotency, dedup

| Concern | Technique |
|---|---|
| Transient provider errors | Exponential backoff with jitter (1 s, 2 s, 4 s, ... cap), max ~5 tries; do not retry 4xx |
| Producer retries | Idempotency key `(producerId, eventId)` stored 24-48 h; duplicates return the original `notifId` |
| Worker crash after sending, before ack | Pass the `notifId` as the provider's own idempotency/collapse key where supported (FCM collapse key, SES message tag) and check status row before sending; accept rare duplicate (**at-least-once**) |
| Poison messages | DLQ after max attempts, alert on DLQ depth |
| Dead push tokens | On `Unregistered`/`NotRegistered` response, delete the token |

Exactly-once across an external provider is impossible; the honest answer is at-least-once plus dedup on our side.

### 5.3 Rate limiting and provider protection

- **Per-user caps** (e.g. max 3 marketing pushes/day) in Redis counters with TTL; the API drops or defers extras. Critical types bypass caps.
- **Per-provider token bucket** in workers so we never exceed SES/Twilio quotas; excess stays in the queue (backpressure) instead of being rejected.
- **Circuit breaker + failover:** if provider A fails or its error rate spikes, route to provider B (e.g. a second SMS vendor) and re-close the breaker after a probe.
- Quiet hours: a delayed queue or scheduler re-enqueues at the user's local morning.

### 5.4 Preferences, templates and scheduling

- Preferences and templates live in Postgres, read through a Redis/local cache with short TTL and invalidation on update, so the hot path avoids the DB.
- Template rendering in the worker (or a template service) with locale fallback; keeps payloads in the queue small.
- Scheduled sends: store in a `scheduled` table keyed by `sendAt` (or use a delay queue/Redis ZSET); a scheduler polls due rows and enqueues. Bulk/audience sends are expanded by a **fan-out job** in batches of ~1K users so one request does not create millions of messages at once.

### 5.5 Status tracking

- Append-only status table/log: `notifId, channel, state (queued, sent, delivered, failed), ts, providerMessageId`. Store in Cassandra/DynamoDB or Postgres partitioned by day; TTL 30-90 days.
- Delivery/open callbacks arrive through provider webhooks into a small ingest service that updates status. Don't put this on the send path.
- Metrics: queue lag per topic, send success rate per provider, end-to-end time for high-priority.

### 5.6 Failure modes

- **Kafka down:** API returns 503; producers retry with their idempotency key. Optionally an outbox table in the producer's DB for transactional safety (write event and "notify" row atomically, relay to API).
- **Provider outage:** breaker opens, messages wait in queue (bounded by retention) or fail over.
- **Redis down:** fall back to the DB for idempotency checks (slower), or fail open for low-priority only.
- **Burst:** autoscale workers on lag; bulk queue is allowed to be slow.

## 6. What interviewers look for

- **Junior:** producers → service → providers per channel, store preferences.
- **Mid:** queue decoupling, per-channel workers, retries/DLQ, idempotency, priority separation.
- **Senior:** head-of-line blocking, provider rate limits and failover, at-least-once reasoning, outbox pattern, token hygiene, scheduled/bulk fan-out, observability.

## 7. Common pitfalls

- Calling providers synchronously from the producer's request
- One shared queue for OTPs and marketing
- Promising exactly-once delivery
- Retrying forever or retrying non-retryable errors
- Ignoring user preferences, opt-outs and per-user frequency caps
- Putting preference/template DB lookups on every send without a cache
