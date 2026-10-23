---
topic: "Booking & Commerce"
difficulty: Medium
problem: "Ticketmaster"
---
# Design Ticketmaster (Event Ticket Booking) – Solution

**Topic:** Booking & Commerce · **Difficulty:** Medium · **Question:** Ticketmaster - Question

## 1. Requirements

**Functional**
- View events (details, venue and seat map with availability)
- Search for events (keyword, date range)
- Book tickets: reserve specific seats for a short period, then confirm by paying

**Non-functional**
- **Consistency for booking:** a ticket is sold at most once (no double booking)
- **Availability** (and low latency) for view and search; search < 500 ms
- Scales to flash-crowd traffic: ~10M concurrent users on a popular event for tens of thousands of seats
- Read-heavy: ~100:1 reads to bookings
- Fairness: no bots or queue jumping for hot events

**Out of scope:** user booking history, admin event creation, dynamic pricing, payment internals (assume a provider with idempotent charge), resale, GDPR, backups, CI/CD.

## 2. Back-of-envelope

- Reads dominate: 100M users x ~10 page views/day ~ 1B reads/day ~ **12K/s avg**, 10x at peaks. Event data is small and cacheable.
- Writes: ~5M tickets/day ~ 60/s on average. Trivial overall; the problem is **one hot event** with millions of requests in the first minute: 5M users x 3 calls ~ 15M requests / 60 s ~ **250K/s** against one inventory of 50K seats.
- Storage: 50K tickets x 100K events/year ~ 5B ticket rows/year x ~100 B ~ **0.5 TB/year**; bookings are smaller. A sharded relational DB handles this; old events can be archived.

## 3. Core entities and API

Entities:
- `Event { id, venueId, performerId, name, description, type, startsAt }`
- `Performer { id, name, bio }`, `Venue { id, name, location, capacity, seatMap (JSON) }`, `User`
- `Ticket { id, eventId, section/row/seat, price, status: AVAILABLE | RESERVED | BOOKED, reservedUntil }`
- `Booking { id, userId, ticketIds[], totalPrice, status: IN_PROGRESS | CONFIRMED }`

```
GET  /events/:eventId                  -> Event + Venue + Performer + Ticket[]
GET  /events/search?keyword=&start=&end=&pageSize=&page=   -> Event[]
POST /bookings/:eventId  { ticketIds } -> { bookingId, expiresAt }   (reserve; 409 if any ticket is taken)
POST /bookings/:bookingId/confirm  { paymentToken }  (Idempotency-Key header)  -> confirmed Booking
```

The booking call starts as one "buy" request and is split into reserve then confirm, so the user can pay while the tickets are held. (Exact path of the confirm step may differ in other write-ups; the two-step shape is what matters.)

## 4. High-level design

!Ticketmaster - Diagram.excalidraw

Basic flow: **Client -> API Gateway / load balancer -> Event Service -> Events DB** for viewing and searching, and **-> Booking Service -> Events DB + payment processor** for booking. All services are stateless, so they scale horizontally behind the load balancer.

- **View/search path:** read-only, served through cache (event details, venue, performer info) and CDN. Event metadata lives in Postgres; search goes to an **Elasticsearch** index fed from the DB by CDC. Stale results by seconds are fine.
- **Booking path:** the **Booking Service** reserves tickets with a TTL in a **Redis distributed lock**, creates the `IN_PROGRESS` booking, charges the card, and only then writes `BOOKED`/`CONFIRMED` in Postgres in a transaction. The DB conditional write is the final arbiter.
- A **virtual waiting queue** (Redis sorted set) sits in front of hot events and admits users at a rate the booking path can sustain.
- A cleanup worker releases expired reservations and keeps the DB and Redis consistent.

## 5. Deep dives

### 5.1 Ticket reservation: preventing double booking

| Approach | How | Verdict |
|---|---|---|
| **Bad:** long-running DB lock (`SELECT ... FOR UPDATE`) | Lock ticket rows during the whole checkout | Locks held across a user's multi-minute checkout; connection exhaustion, deadlock risk |
| **Good:** status field + expiry + cron | Set `RESERVED` with `reservedUntil`; a cron job flips expired rows back to `AVAILABLE` | Simple, but tickets stay unavailable until the next cron run (unlock lag) |
| **Great:** implicit status | Treat a ticket as available if it is `AVAILABLE` **or** `RESERVED` with `reservedUntil < now`; no cleanup needed, only short transactions | No lag, but every read path (seat map) must apply the same rule; complexity in queries |
| **Great (recommended):** distributed lock with TTL (Redis) | `SET ticket:{event}:{ticket} {bookingId} NX EX 600`; TTL frees abandoned tickets automatically | Fast, minimal DB contention, handles abandonment; the seat-map read must merge lock state with DB state |
| Optimistic concurrency | `UPDATE tickets SET status='BOOKED' WHERE id=? AND status<>'BOOKED'` | Excellent as the *final* write; alone it makes hot seats thrash with retries |

**Recommended flow:** Step 1 (reserve): for every requested ticket do an atomic `SET NX EX`, in one Lua script for multi-ticket requests so it is all-or-nothing. Step 2 (confirm): charge, then in one Postgres transaction `UPDATE tickets SET status='BOOKED' WHERE ... AND status<>'BOOKED'` and mark the booking `CONFIRMED`. Even if Redis loses a key, no double sale is possible.

!Ticketmaster - Deep Dive Diagram.excalidraw

Lifecycle details:
- The TTL (e.g. 10 min) is the checkout window; the client shows a countdown from `expiresAt`.
- If the user abandons, the key expires on its own and the ticket is available again. A keyspace notification or periodic sweeper fixes up DB rows and pushes an availability event.
- **Payment succeeds after the reservation expired:** the conditional write fails (or someone else re-reserved it). Refund automatically, or verify ownership before charging and extend the TTL for the duration of the payment call.
- **Redis failure:** fail closed for hot events (stop new reservations) or rebuild from `RESERVED` rows. DB writes are the arbiter, so correctness survives.
- Confirm is **idempotent** via an idempotency key, so a retry does not charge twice.

### 5.2 Scaling view and search reads

This is the standard "scaling reads" pattern. Event details, venue info and performer bios change rarely, so put them behind a **cache** (Redis/Memcached; e.g. a TTL of hours up to a day) and a CDN for static parts, load balance, and scale the stateless Event Service horizontally. Read replicas of Postgres absorb cache misses.

### 5.3 The high-demand event experience: live seat map and waiting queue

- **Good: push the seat map with SSE.** Clients get real-time updates for tickets that become reserved or booked (or poll every few seconds), so users stop clicking dead seats. Slightly stale maps are fine because the reserve step is authoritative and returns 409.
- **Great: virtual waiting queue.** Users enter a Redis-backed queue (sorted set) before the booking page; the system admits N users per interval based on remaining capacity, with SSE/WebSocket pushing position updates. Use a random position or a fair rule (not first-come-first-served by millisecond, which favors bots); admission tokens are signed and short-lived and the booking API rejects requests without one. This turns a ~250K/s spike into a flat ~1-2K/s of admitted users that ordinary scaling can handle.
- Serve availability as a compact bitmap/JSON cached in Redis (and CDN with a 1-2 s TTL), not per-seat DB queries. Offer "best available" to spread contention across the venue.
- Anti-scalper add-ons: rate limits per user/IP/device, CAPTCHA, verified-fan pre-registration, per-user ticket limits.

### 5.4 Improving search performance

| Approach | Verdict |
|---|---|
| **Good:** SQL indexes on name, date, performer, location; query tuning (`EXPLAIN`, `LIMIT`) | Fine at small scale; `LIKE '%kw%'` still does not use indexes and cannot rank |
| **Good:** Postgres full-text index (`tsvector` + GIN) | Better text search without a new system; limited fuzziness/relevance tuning |
| **Great (recommended):** **Elasticsearch** with an inverted index, fed from Postgres through **CDC** (e.g. Debezium) | Fast, typo-tolerant/fuzzy, relevance ranking, geo and date filters; eventual consistency of a few seconds is acceptable |

Elasticsearch is a derived read model: Postgres stays the source of truth.

### 5.5 Caching search results

- **Good:** cache query results in Redis/Memcached keyed by the normalized query. Challenge: invalidating stale results when events change (short TTLs help).
- **Great:** lean on Elasticsearch's own shard-level query/request caches, plus **CDN edge caching** for non-personalized, popular queries (e.g. "top events in Berlin this weekend").

### 5.6 Data and scaling

- Partition tickets by `eventId` so one event's contention stays on one shard, and a hot event can get its own shard or Redis node. Bookings partition by `userId`.
- A Kafka topic carries `TicketBooked` / `BookingConfirmed` events for emails, e-tickets (signed QR codes) and analytics.

## 6. What interviewers look for

- **Mid-level (breadth, little depth):** sensible entities and API, a functional high-level design for viewing and booking, the "Good" solution for no double booking (status + expiry + cron), search with basic indexes; the interviewer probes and steers the deep dives.
- **Senior (more depth in 2-3 areas):** advanced solutions (distributed lock with TTL, Elasticsearch with CDC, caching and sharding), clear trade-offs, two-step reserve then confirm with the DB as arbiter, payment-timeout races, waiting queue and fairness, proactively spotting problems.
- **Staff+ (mostly depth):** independently finds and solves the hard problems from real-world experience (hot-shard handling, Redis failure modes, bot defence, consistency boundaries), proposes innovative approaches, and needs minimal steering.

## 7. Common pitfalls

- Holding a DB lock or transaction open for the whole checkout
- A Redis reservation as the only source of truth, with no DB conditional write
- No answer for "payment succeeded but the reservation expired"
- Adding more servers as the only answer to an on-sale spike
- Strong consistency for search and browse, which does not need it
- A waiting queue ordered by arrival time, which hands every ticket to bots
