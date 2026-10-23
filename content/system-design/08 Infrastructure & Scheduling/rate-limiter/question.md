---
video: https://www.youtube.com/watch?v=MIJFyUPG4Z4
topic: "Infrastructure & Scheduling"
difficulty: Medium
problem: "Rate Limiter"
---
# Design a Rate Limiter

**Topic:** Infrastructure & Scheduling · **Difficulty:** Medium · **Answer:** Rate Limiter - Solution

## Prompt

Design a distributed rate limiter that protects an API fleet. Each incoming request is either allowed or rejected (HTTP 429) based on how many requests the caller has recently made. The limiter must work across many gateway or application instances and must not become the bottleneck or the single point of failure.

## Requirements to pin down (ask the interviewer)

- What do we limit by: user id, API key, IP address, endpoint, or a combination? Are limits different per tier (free / paid)?
- Hard limit (reject) or soft limit (throttle / queue / degrade)?
- Is a small amount of over-admission acceptable, or must the limit be exact?
- Single region or multi-region? Where does the check live: client, gateway, or each service?
- Can rules change at runtime without a deploy?

## Scale hints

- ~1M requests per second at peak across the fleet, ~100M daily active users
- Added latency budget: under ~10 ms per check (a few ms at p99 ideally)
- High availability matters more than perfect accuracy (eventual consistency is acceptable)
- If the limiter is down, the product must keep working (decision needed: fail open or closed?)

## Think about before opening the answer

1. What are the main algorithms (fixed window, sliding window, token bucket, leaky bucket) and what does each get wrong?
2. Where do you keep the counters, and how do you make "read, decide, update" atomic across many instances?
3. Where does the limiter live (in-process, separate service, API gateway), and how do you identify the caller?
4. How do you shard the counter store, and what happens to a single very hot key?
5. What do you tell the client when it is rejected, and what should well-behaved clients do?
6. What happens when the counter store is unreachable, or when you run in several regions, and how do you change rules at runtime?

## Self-check

- [ ] I can describe token bucket state and its refill math
- [ ] I can explain the boundary-burst problem of fixed windows
- [ ] I can justify fail-open vs fail-closed for a given product
- [ ] I can estimate memory and ops/s for the counter store
