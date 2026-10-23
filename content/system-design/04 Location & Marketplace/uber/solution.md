---
topic: "Location & Marketplace"
difficulty: Hard
problem: "Uber"
---
# Design Uber (Ride Hailing) – Solution

**Topic:** Location & Marketplace · **Difficulty:** Hard · **Question:** Uber - Question

## 1. Requirements

**Functional**
- Rider gets a fare and ETA estimate for a pickup/destination pair
- Rider confirms the fare and requests a ride; the system matches a nearby available driver
- Driver is offered the ride and can accept or decline; on accept they get the pickup location for navigation
- Rider and driver see each other's live location during pickup and trip (extension beyond the core four)

**Non-functional**
- Location updates are very write-heavy and may be slightly stale (seconds), but matching must be fast: a match within about a minute, or a clean "no drivers" failure
- **Strong consistency for assignment:** a driver gets one active ride, a ride gets one driver, never two simultaneous offers to the same driver
- **High throughput at a hot spot:** ~100K concurrent ride requests from one location (stadium letting out)
- High availability per city; a lost location update is harmless, a lost ride is not
- Durable ride and payment records; real-time state can be rebuilt

**Out of scope:** post-trip ratings, advance scheduling, ride categories (X / XL / Comfort), payments, pooling, driver onboarding, fraud (mention as extensions).

## 2. Back-of-envelope

- 1M online drivers / 4 s ≈ **250K location writes/s** at peak (at 10M drivers and one ping per 5 s it is ~2M/s, so the same conclusion holds, only more shards). At ~100 B each that is ~25 MB/s, trivial for bandwidth but far too chatty for a relational DB.
- Live index: 1M drivers × ~100 B ≈ 100 MB. The whole "where is everyone now" state fits in the RAM of a single node. Shard anyway, for write throughput and failure isolation.
- 20M rides/day ≈ 230/s average, ~1-2K/s at peak. That is a small transactional load, so ride state can live in a normal sharded SQL DB.
- Location history for analytics: 250K/s × 86,400 s × 100 B ≈ 2 TB/day, which goes to Kafka then object storage, not the OLTP DB.

## 3. Core entities and API

Entities: `Rider { id, paymentMethods }`, `Driver { id, status, vehicle }`, `Fare { id, riderId, pickup, dest, estimate, etaMin, route }`, `Ride { id, riderId, driverId?, fareId, pickup, dest, state, timestamps }`, `Location { driverId, lat, lng, ts }`.

```
POST /fare             { pickup, dest }              -> { fareId, fare, etaMin }
POST /rides            { fareId }                    -> { rideId, state: REQUESTED }
POST /drivers/location { lat, lng, heading }         (every ~4 s, over WebSocket or HTTP)
PATCH /rides/{rideId}  { action: accept|decline }    (driver side; accept returns pickup coordinates)
WS   /rides/{rideId}/events                          (state changes, driver position)
```

The driver identity comes from the auth token (JWT), never from the body, and the rider is derived the same way. Riders poll or subscribe to the ride by id. Persisting the `Fare` is what lets the rider pay the quote they saw.

## 4. High-level design

!Uber - Diagram.excalidraw

- **Fare path:** the Ride Service calls a third-party **mapping API** for distance and ETA, computes the price, and stores a `Fare` record (`POST /fare`).
- **Location path:** driver apps stream pings to the Location Service, which writes only to an in-memory geo index (Redis GEO/H3 cells, with a TTL so crashed drivers vanish). A copy goes to Kafka asynchronously for history, ETA models and surge.
- **Ride path:** Ride Service validates the `fareId`, writes the ride (`REQUESTED`) to the Rides DB and hands it to Matching.
- **Matching:** queries the geo index, ranks candidates, reserves one driver with a lock and asks the **Notification Service** to send the offer (WebSocket, falling back to APNs/FCM push). Acceptance moves the ride to `ASSIGNED` and returns the pickup coordinates to the driver.
- Services are stateless; each city/region runs a cell with its own index so a failure stays local.

## 5. Deep dives

### 5.1 Ingesting and indexing driver locations

| Approach | How | Pros | Cons |
|---|---|---|---|
| Relational DB with lat/lng + index | `UPDATE drivers SET lat, lng` | Simple, PostGIS queries | 250K updates/s of hot-row churn; index maintenance kills it |
| Geohash string prefix | Cell key = geohash(lat, lng, precision 6) | Works on any KV store, prefix search | Cell shapes distort with latitude; neighbour lookup at borders is fiddly |
| Quadtree (in memory) | Adaptive cells split when dense | Handles dense downtown well | Rebalancing, harder to distribute, custom code |
| **H3 hex cells or Redis GEO** (the "great" option) | Hash drivers into hex cells; query the ring of cells around the rider | Uniform neighbours, easy radius query, in-memory | Need to pick resolution; sharding is by city/cell |

In interview-rubric terms: writing every ping straight to the DB and scanning is the **bad** answer; batching writes into PostGIS is **good**; an in-memory geo index (Redis GEO or H3 cells with TTL) is **great**. Run it with Sentinel or replicas for availability. A lost index is rebuilt from the next round of pings.

**Recommended:** an in-memory index sharded by city (or by H3 parent cell). Redis `GEOADD`/`GEOSEARCH` is the simplest start. With H3 at resolution ~8 (≈0.7 km² cells), keep one set per cell holding available drivers; a query reads the rider's cell plus the k-ring neighbours.
- Writes are idempotent and last-write-wins, so no coordination is needed. A driver moving across cells is a delete from the old cell plus an add to the new one.
- Each entry has a TTL (e.g. 10-15 s). If pings stop, the driver drops out of the index on its own. **Adaptive ping rate** (faster when on a trip or near an intersection, slower when idle) cuts load a lot.
- **Overload control:** pings are the biggest load, so make the client decide when to send. The adaptive interval above (speed, heading, distance to a likely request, battery/sensors) is a client-side change that removes most traffic without hurting match quality.
- Persisting every ping to a DB is the common mistake. The index is a cache of "now" and can be rebuilt from the next round of pings within seconds after a crash.

### 5.2 Matching without double-booking

Matching is the hard part. Flow (see the diagram below):
1. Query candidate drivers within ~3 km (grow the radius if too few).
2. Rank by **ETA to pickup** from the routing service (road distance, not straight line), with straight-line distance as a cheap pre-filter, then by acceptance rate or rating.
3. **Lock** the best candidate: `SET driver:{id}:lock {rideId} NX PX 10000` in Redis (TTL = the 10 s offer window). If it fails, the driver is already being offered something, so take the next one.
4. Push the offer to the driver. If they accept, transition the ride to `ASSIGNED` with a conditional DB update (`WHERE state = 'REQUESTED'`), mark the driver busy and release the lock. If they decline or the TTL expires, release and try the next candidate.

!Uber - Deep Dive Diagram.excalidraw

Ways to prevent a driver being offered two rides:

| Approach | Verdict | Why |
|---|---|---|
| In-memory lock inside one matching instance | Bad | Other instances do not see it; breaks as soon as there are 2 workers |
| Status column in the DB (`AVAILABLE` to `OFFERED`) plus a cleanup timeout | Good | Durable and consistent, but a crash leaves the driver stuck until a sweeper runs, and it adds write load |
| **Distributed lock in Redis with a ~10 s TTL** | Great | Atomic `NX`, expires on its own if the worker dies, fast |

Design choices:
- **Sequential vs parallel offers.** Offering to one driver at a time is fair and simple but slow when drivers ignore offers. Offering to 2-3 at once speeds things up but needs a first-wins check. The conditional update on the ride row is that check, and the losers get "ride no longer available".
- **The lock TTL is the safety net.** If the matching worker crashes mid-offer, the lock expires and the driver becomes available again. No cleanup job needed.
- A Redis lock is not a perfect mutex across failover. That is acceptable here because the **ground truth** is the conditional write in the Rides DB (one driver per ride) plus a driver-state check. The lock only reduces wasted offers.
- Matching workers are partitioned by city so one ride request is handled by one worker at a time.

**Not dropping requests at peak.** First-come-first-served with no buffer (**bad**) loses requests when matching is slow or a worker dies. Put ride requests on a **Kafka** topic partitioned by region/cell. A worker commits the offset only after the request is matched (or has definitively failed), so a crash simply replays it. Scale by adding consumers (and partitions). A managed service (MSK/Confluent) saves operations work.

**Driver never answers.** Sleeping a thread for 10 s and trying the next driver is fragile. A **delay queue** that re-enqueues the ride after 10 s is **good**; a **durable execution** engine (Temporal, AWS Step Functions) running "offer, wait 10 s or accept, next driver" is **great**: timers and progress survive restarts, and the business logic reads as straight-line code. The cost is a new infrastructure dependency.

### 5.3 Ride lifecycle and durability

State machine: `REQUESTED → MATCHING → ASSIGNED → PICKUP → IN_PROGRESS → COMPLETED` (plus `CANCELLED`, `NO_DRIVERS`). Store it in a SQL DB (Postgres, or Spanner/CockroachDB for multi-region), sharded by `rideId` or city. Only legal transitions are allowed, each as a conditional update.
- For long, failure-prone workflows (match → offer → retries → timeouts) a **durable workflow engine** (Temporal, or a state table + timers) beats hand-rolled cron polling: timers and retries survive a restart.
- Each transition is an event on Kafka (outbox pattern) for notifications, billing and analytics.
- Live trip position during a ride is written to the Location path, not to the Rides DB. A trimmed route is stored at the end.

### 5.4 Delivering offers and live updates

- The **Notification Service** owns delivery. Driver and rider apps keep a **WebSocket** (or gRPC stream) to an edge gateway. Matching sends the offer through a connection registry (`driverId → gatewayNode` in Redis) and falls back to APNs/FCM push when the socket is down.
- Offers carry an expiry and an idempotency id so duplicate deliveries are harmless.
- During a trip, the rider receives the driver's position via the gateway (subscribe to the driver's updates, throttled to 1 per 2-4 s) rather than polling.

### 5.5 Fare, ETA and surge

- Fare estimate = base + distance × rate + time × rate, multiplied by a **surge factor** per H3 cell. Surge is computed by a streaming job (Kafka → Flink) as `open requests / available drivers` per cell over a sliding window, cached and read by the estimate API. Store the quoted fare as the `Fare` record (`fareId`) so the rider pays what they saw.
- ETAs come from a routing service (graph + live traffic), which is a separate system. Cache popular origin/destination cell pairs.

### 5.6 Scaling and failure modes

- **Latency and throughput.** Vertical scaling (**bad**) is costly and a single point of failure. **Geo-shard** instead: each region has its own services, Kafka, Redis and DB (with read replicas), so clients talk to a nearby stack. Use consistent hashing so shards can be added; a scatter-gather query is only needed near a shard boundary (a rider close to a cell edge).
- **Hot spots** (stadium, airport, the ~100K-requests-at-one-spot case): shard the index by H3 cell, split a hot cell into children, and queue requests per cell. Add queuing/virtual waiting rather than failing requests.
- **Regional failover:** cities are cells. If a cell's Redis dies, drivers re-register within seconds via the next ping. Rides are in the replicated SQL store.
- **Stale or lying GPS:** reject out-of-order timestamps, impossible speeds and cache coarsened positions for riders.
- **Rider cancels mid-offer:** the conditional update on state means a late acceptance fails cleanly and the driver is released.

## 6. What interviewers look for

- **Mid-level:** clear entities and APIs, a working high-level design for fare, request, match and accept, the need for a spatial index (even if not named), and at least a "good" answer to double-booking (a DB status plus timeout, ideally a Redis lock).
- **Senior:** moves quickly through the basics and goes deep on 2+ topics: write-rate estimation, in-memory geo index with TTL, lock plus conditional-update for correctness, Kafka buffering, workflow/state machine, hot-cell handling, with explicit pros and cons.
- **Staff+:** about 60% depth. Covers 3+ areas with real-world insight and proactively raises the problems: adaptive client pings, durable execution for offers, geo-sharded cells and regional failover, surge, GPS abuse, and operational concerns. The interviewer should learn something.

## 7. Common pitfalls

- Writing every GPS ping to the main SQL database
- Using straight-line distance only for ranking, ignoring the road network
- No mechanism for a driver ignoring an offer (no timeout/lock expiry)
- No buffer for ride requests, so peak load or a crash silently drops them
- Vertical scaling instead of geo-sharding
- Treating the Redis lock as the only guard, instead of a conditional write on durable state
- A single global index with no sharding by region
- Polling from the client for offers and positions instead of a push channel
