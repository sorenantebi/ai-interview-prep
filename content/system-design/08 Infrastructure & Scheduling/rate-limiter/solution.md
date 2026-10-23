---
topic: "Infrastructure & Scheduling"
difficulty: Medium
problem: "Rate Limiter"
---
# Design a Rate Limiter – Solution

**Topic:** Infrastructure & Scheduling · **Difficulty:** Medium · **Question:** Rate Limiter - Question

## 1. Requirements

**Functional**
- Identify the caller (user ID, API key, or IP address) and the resource, and decide allow or deny
- Support multiple rules per request (e.g. 100/min per user and 10/s per IP and 1000/min per endpoint), configurable per tier
- Reject with HTTP 429 plus information the client can act on (`Retry-After`, remaining quota)

**Non-functional**
- Very low overhead: < 10 ms per check (aim for ~1-5 ms p99)
- Highly available: a limiter outage must not become a site outage; **eventual consistency is acceptable** across nodes
- Accurate enough: small over-admission is fine, large drift is not
- Scale: ~1M checks/s across ~100M daily active users (~100M active keys); rules changeable at runtime

**Out of scope:** DDoS mitigation at L3/L4 (that belongs to the CDN / WAF), complex analytics on limiter data, long-term persistence of counters, strong consistency, billing-grade metering, per-request cost estimation.

## 2. Back-of-envelope

- Token bucket state per key: `tokens` (float) + `lastRefill` (timestamp) ≈ 16 B payload, ~50-100 B with Redis key and overhead.
- 100M keys × ~80 B ≈ **8 GB**. Fits in memory on a handful of nodes. Keys that go idle expire via TTL (e.g. ~1 h), so the live set is much smaller and there is no memory leak.
- Throughput: 1M checks/s. A single Redis node does roughly 50-100K+ rate-limit checks/s (Lua scripts somewhat fewer), so plan **~16-32 shards** with headroom for rule fan-out (a request that hits 3 rules means 3 bucket reads).
- Memory is a non-issue; **ops/s and hot keys** are the real constraints.

## 3. Core entities and API

Entities: `Rule { id, match (route, tier, key type), limit, windowSec, burst, algorithm }`, `Client` (the user / IP / API key being limited, with its bucket state `{ key, tokens, lastRefillTs }`), `Request` (the incoming call evaluated against the applicable rules).

```
isRequestAllowed(clientId, ruleId) -> { passes, remaining, resetTime }   // internal call or library
Response on deny:  429 Too Many Requests
                   Retry-After: 12
                   X-RateLimit-Limit: 100   X-RateLimit-Remaining: 0   X-RateLimit-Reset: <epoch>
PUT /admin/rules/{id}   { limit, windowSec, burst }                    // rules store
```

Client identification: JWT user ID for authenticated calls, `X-API-Key` for developer APIs, client IP (`X-Forwarded-For`, taken from the trusted proxy hop) for anonymous traffic. A request often matches several rules; the most restrictive one wins.

Key format: `rl:{ruleId}:{callerId}` (+ window index for window-based algorithms).

## 4. High-level design

!Rate Limiter - Diagram.excalidraw

- **Placement.** Inside each app server as local counters (**bad**) cannot enforce a global limit. A dedicated rate-limit service (**good**) gives global state and room for business logic, but costs an extra network hop. **Middleware in the API gateway (great, chosen)** checks every request once at the edge and shields everything behind it, at the price of seeing only request-level context.
- The limiter runs as that **middleware in the API gateway** (or a sidecar), so every request is checked once, before any backend work is done.
- Rules live in a small rules store, are cached in each gateway process and refreshed by push or short polling. A request never waits on the rules store.
- Counters / buckets live in a **sharded Redis cluster**. The check is a single round trip running one Lua script, which keeps read-modify-write atomic.
- Allowed requests continue to the backend. Denied requests return 429 straight from the gateway (fail fast, no queuing, which avoids memory build-up and retry cascades). Every decision emits a metric.

## 5. Deep dives

### 5.1 Choosing the algorithm

| Algorithm | State per key | Behaviour | Weakness |
|---|---|---|---|
| Fixed window counter | 1 counter | Simple, `INCR` + `EXPIRE` | Boundary burst: 100 at 12:00:59 and 100 at 12:01:00 gives 200 in 2 s |
| Sliding window log | Sorted set of timestamps | Exact | Memory O(limit) per key; expensive for 10K/min limits |
| Sliding window counter | 2 counters (current + previous window) | Weighted estimate `prev × overlap + cur`, ~1% error | Approximate (usually fine) |
| **Token bucket** | tokens + last refill | Allows bursts up to bucket size, steady rate = refill rate | Two parameters to tune |
| Leaky bucket | queue or level | Smooth output rate | Bursts get queued or dropped, adds latency if queued |

**Recommended:** token bucket as the default (it is what users expect: "10/s with bursts of 50"), sliding window counter where a strict "N per minute" reading is needed. Refill is computed lazily on each check: `tokens = min(burst, tokens + (now - lastRefill) × rate)`, then take `cost` if available. No background refill job.

### 5.2 Atomicity across instances

Naive `GET` then `SET` from many gateways loses updates and over-admits. Options:

- **Lua script in Redis (chosen):** refill, compare, decrement and `PEXPIRE` happen in one atomic server-side step, one round trip. Use the Redis server clock (`TIME`) inside the script so gateway clock skew does not matter.
- `INCR` for fixed windows only: naturally atomic, but only fits that algorithm.
- Optimistic transactions (`WATCH/MULTI`): retries under contention, worse for hot keys. A plain `HMGET` read outside the transaction followed by `MULTI/EXEC` is a race: two gateways can both read the same token count and both be admitted.
- Distributed locks: far too slow and creates new failure modes. Reject.

### 5.3 Sharding and hot keys

- Shard by `hash(key)` (Redis Cluster's 16,384 hash slots, or consistent hashing in the client). One shard handles ~50-100K+ checks/s, so 1M/s needs roughly 10+ shards plus headroom. All state for one key lives on one shard, so no cross-node coordination per check.
- A single hot key (one abusive IP, one huge customer) is capped by one shard's ops/s. For **legitimate heavy clients**: client-side throttling in the SDK, batching several operations into one call, and premium tiers with higher limits or dedicated capacity. For **abusive traffic**: auto-block after repeated violations (a Redis-backed blocklist) and pre-filter at a DDoS service (Cloudflare, AWS Shield); account-level limits complement per-IP limits behind shared NATs. Other mitigations: **local pre-checks** (a per-gateway in-memory bucket that takes batches of tokens, e.g. 10% of the global limit, from Redis) so most requests skip the network; split a key into N sub-keys with the limit divided by N for very large tenants; block known-bad IPs at the CDN/WAF so they never reach the limiter.
- Rebalancing: add shards gradually. Losing counters during a reshard simply means callers briefly get a fresh budget, which is acceptable.

### 5.4 Failure modes: fail open or closed

- Counter store down or slow (> 5-10 ms): the gateway uses a **timeout plus circuit breaker**.
- **Fail open** (allow) for normal product traffic: availability matters more than strictness. Fall back to a coarse local in-memory limiter per gateway so a total outage is not unlimited.
- **Fail closed** (reject) for abuse-sensitive routes (login, SMS / OTP send, password reset), where over-admission has real cost. Some high-traffic platforms go fully fail-closed because a Redis outage often coincides with a traffic spike that would flatten the backends. Either is defensible: state the trade-off and pick per route.
- Run each shard as a primary plus replica(s) with automatic failover (Redis Cluster does this natively) and monitor shard health.
- Redis replication is asynchronous: a primary failover can lose the last few updates. Callers get a slightly larger budget for a moment. Not worth synchronous replication on the hot path.

### 5.5 Multi-region and consistency

- Exact global limits across regions would cost a cross-region RTT per request. Do not do that.
- Pattern: each region enforces locally on a **share of the global limit** (e.g. 40/30/30), and a background sync rebalances the shares based on observed traffic. Or route each caller to a home region.
- Accept bounded error: at most ~(regions × sync interval × rate) over-admission.

### 5.6 Latency and dynamic rules

- **Latency:** persistent, pooled connections from gateways to Redis (a new TCP handshake can cost 20-50 ms and would blow the budget); deploy gateways and Redis in the same region, ideally the same AZ. Local caching of decisions, batching requests or batching Lua calls are second-order and add error or complexity.
- **Rule changes:** gateways **poll** the rules store (e.g. every ~30 s) is simple (**good**) but changes lag by the interval. A **push** channel from a configuration service (ZooKeeper / etcd watches) (**great**) applies emergency limits within seconds, at the cost of another system and partial-failure handling. Either way rules are cached in memory, so a check never waits on the rules store.

### 5.7 Client experience and operations

- Return `429` with `Retry-After`. Clients should use exponential backoff with jitter, otherwise synchronized retries create a thundering herd.
- Soft actions are possible: degrade (serve cached/lower quality), queue, or tag the request instead of rejecting.
- Shadow mode for new rules: log would-be denials without enforcing, then switch on.
- Dashboards for deny rate per rule, top limited keys, limiter latency, Redis ops/s per shard.

## 6. What interviewers look for

- **Mid-level:** explains token bucket, puts the limiter in the API gateway, uses Redis for shared state, recognises that one Redis will not do 1M/s so it must shard. Handles follow-ups on the components.
- **Senior:** compares algorithms and placements, understands consistent hashing / Redis Cluster, insists on atomic updates (Lua), discusses fail-open vs fail-closed unprompted, and raises hot keys, latency (pooling) and dynamic rules, with quantified ops/s.
- **Staff+:** about 60% depth from production experience: multi-region budget split and consistency trade-offs, clock handling, observability and rollout (shadow mode) without being asked, strong opinions with real incidents behind them. Often this question is too easy for this level.

## 7. Common pitfalls

- Non-atomic read then write, or relying on gateway clocks
- Locking per request (kills latency and availability)
- One global counter key for everything, creating a hot shard
- Forgetting the failure story: limiter outage taking the API down
- Fixed window only, without acknowledging the 2x burst at the boundary
- Returning 429 with no `Retry-After`, inviting retry storms
