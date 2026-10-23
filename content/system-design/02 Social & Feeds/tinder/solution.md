---
topic: "Social & Feeds"
difficulty: Medium
problem: "Tinder"
---
# Design Tinder – Solution

**Topic:** Social & Feeds · **Difficulty:** Medium · **Question:** Tinder - Question

## 1. Requirements

**Functional**
- Create a profile with preferences (age range, interests, max distance)
- View a stack of potential matches filtered by the user's location and preferences
- Swipe right (like) or left (pass) on a candidate
- Get notified when a swipe is mutual (a match)

**Non-functional**
- **Strong consistency for swiping**: a mutual like must never be missed, even when both users swipe at the same instant
- Candidate stack (feed) generation < 300 ms; swipes acknowledged quickly (~100 ms)
- Never re-show a profile the user already swiped
- Scale: 20M DAU at ~100 swipes per user per day = ~2B swipes/day; eventual consistency is fine for profile edits and location

**Out of scope:** photo upload, direct messaging/chat, premium features (super swipes, payments), the ML ranking model, fraud/bot detection, monitoring.

## 2. Back-of-envelope

- Swipes: 20M × 100 = 2B/day ≈ **23K/s average, ~100K/s peak**.
- Swipe record: swiperId + targetId + direction + timestamp ≈ 30 B raw, ~100 B with keys and overhead. 2B × 100 B = **~200 GB/day ≈ 73 TB/year**, fine for a sharded wide-column store but too big to keep forever in Redis.
- Candidate requests: a stack of ~100 profiles per fetch, ~one fetch per 100 swipes → ~230 fetches/s average. Low QPS but heavy per request.
- Geo index: only **active** users need to be searchable, ~20M entries × 200 B ≈ 4 GB. Fits in memory and shards by region.
- Photos dominate bytes (5 to 9 per profile, a few hundred KB each), so serve them from S3 behind a CDN and keep them out of every other path.

## 3. Core entities and API

Entities: `User { userId, bio, birthdate, gender, prefs (age range, interests, maxDistance), lastLocation }`, `Swipe { swiperId, targetId, decision, ts }`, `Match { userA, userB, createdAt }`.

```
POST /profile                                  { bio, prefs, ... }        -> 200
GET  /feed?lat={lat}&long={long}&distance={km}                            -> { profiles[] }
POST /swipe/{userId}                           { decision: yes | no }     -> { matched: bool }
```

The feed request carries the current location, which also refreshes the user's stored location (no separate location endpoint needed). The swipe response carries `matched` so the client can show the "It's a match" screen immediately for the second swiper; the first swiper is told by push.

## 4. High-level design

!Tinder - Diagram.excalidraw

- **Profile Service** owns profile and preferences in the User DB (Postgres: small, relational, rarely written), photos in S3 behind a CDN.
- **Feed Service** returns the candidate stack: first from a precomputed stack in the Feed Cache, otherwise by querying the Geo Index (Elasticsearch) for users within the radius and matching filters, removing already-seen ids, and returning a batch. The client prefetches the next batch before the stack runs out.
- **Swipe Service** records the swipe, checks for the reverse swipe, creates the match, and emits a match event to the Notification Service (push via APNs/FCM and an in-app WebSocket if the other user is online). The swipe store is Cassandra (with Redis in front for atomic match detection, see 5.3).

## 5. Deep dives

### 5.1 Low-latency feed generation

Real-time geo queries over millions of users with attribute filters are too slow to run naively on every request, so the options are:

| Approach | Verdict | Trade-offs |
|---|---|---|
| Query the primary DB with lat/lng range plus filters | Bad | One B-tree range only, poor 2D selectivity, full scans at scale |
| Indexed search store (Elasticsearch/OpenSearch `geo_distance` + age/gender filters) | Good | One query does distance and filters; needs change-data-capture to stay in sync with the User DB, write-heavy indexing, near-real-time |
| Precompute stacks in a background job and cache per user | Good | Instant load; stacks go stale (people move, change prefs) and a heavy user can exhaust the stack |
| **Hybrid: precomputed cache plus indexed DB** | **Great** | Cache serves the first load instantly; the index serves exhausted stacks and cache misses; a strict TTL (under ~1 h) plus a refresh on location or preference change controls staleness |

**Recommended: the hybrid.** Details of the index itself follow.

#### Finding nearby candidates (index choices)

| Approach | How | Pros | Cons |
|---|---|---|---|
| SQL with lat/lng range and B-tree | `WHERE lat BETWEEN ... AND lng BETWEEN ...` | Simplest | One index range only, poor for 2D, slow at scale |
| Geohash / S2 cell index in Redis or KV | Key = cell id, value = set of user ids; query the user's cell plus neighbors | Fast, cheap, easy to shard by cell prefix | Boundaries and varying density need multi-resolution cells |
| **Elasticsearch / OpenSearch geo + filters** | `geo_distance` filter plus age/gender filters, sorted by activity score | One query combines distance and attribute filters | Heavier infrastructure, near-real-time (seconds) indexing |
| Quadtree service | Adaptive cells by density | Good for hot cities | Custom code to build and keep consistent |

**Recommended index:** an S2/geohash-sharded index (Elasticsearch shards routed by region, or Redis for the hot set), with **adaptive cell size** (small cells in dense Manhattan, large in rural areas). Only users active in the last N days are indexed. Location updates are throttled (only reindex when the user moved > ~1 km or after several minutes), because a dating app does not need second-level freshness. Candidate stacks are **precomputed in batches** by a background job and cached per user (TTL under an hour), re-computed on a schedule and when location or preferences change; ES serves users who exhaust the cached stack.

### 5.2 Never show the same profile twice

Per user the seen set grows to tens of thousands of ids, and a plain database check is both expensive and (on an eventually consistent NoSQL store) can miss very recent swipes. Options:

| Option | Verdict | Pros | Cons |
|---|---|---|---|
| Query the swipe store and exclude in the DB (contains check) | Bad | Exact, no extra state | Extra read per candidate fetch, huge exclusion lists, availability gaps on NoSQL |
| **Client-side cache of recent swipes** plus the DB query | **Great** | The device filters what it swiped recently, cheap, hides replication lag | Assumes a single device per user; reinstall or a second phone loses it |
| **Per-user Bloom filter in Redis** (for heavy swipers) | **Great** | Tiny (~10 bits per id, so ~50 KB for 40K swipes at 1% FP), O(1) checks, zero false negatives so a seen profile is never shown again | False positives permanently hide a few good profiles (tune the rate); cannot delete; one more cache to manage and rebuild |
| Redis set of seen ids | Good | Exact | Memory heavy: 40K × 8 B × 20M users is ~6.4 TB |

**Recommended:** client-side cache for recent swipes, and a Bloom filter once a user's history passes a size threshold, applied as a first filter over the feed candidates (over-fetch by ~30%). The durable swipe store is the source of truth to rebuild the filter. Optionally let left-swiped profiles reappear after months. Staff+ depth: size the filter for the target false-positive rate per user and decide how a user rebuilds it when it saturates.

### 5.3 Swipe and match detection (consistent, low-latency swiping)

The hard part is two users swiping on each other at the same moment, at 2B swipes/day.

| Approach | Verdict | Trade-offs |
|---|---|---|
| Write swipes, then poll the DB for mutual likes | Bad | Delayed notifications and heavy DB load |
| Database transaction across both swipe rows | Good | Correct, but Cassandra lightweight transactions cannot span partitions |
| **Cassandra with a compound partition key** `(min(A,B), max(A,B))` | **Great** | Both directions of a pair live in one partition, so one single-partition transaction (LWT) is atomic; swipes by one user are spread over many partitions |
| **Redis with a Lua script** | **Great** | Script atomically records the swipe and checks the reverse one; shard with consistent hashing on the sorted pair so both swipes hit the same node; needs a durable Cassandra copy behind it |

**Recommended:** Redis (Lua) for the atomic check plus Cassandra for durability. For A swiping right on B, in one script keyed by the sorted pair: record `A→B`, read `B→A`, and if both are likes return "matched". Only right swipes need to live in Redis (left swipes go straight to the durable store), with a TTL or eviction policy; a miss falls back to Cassandra. After the script returns, persist the swipe to Cassandra (partition key `swiperId`) asynchronously.

Fallback without Lua: always write first, then read. With write-then-read, at least one of the two requests sees the other's swipe (possibly both do), which closes the race where both read before either write lands. Because both may then try to create the match, the match key is the **sorted pair** with insert-if-not-exists (LWT or unique constraint), and only the creator publishes the event. This also makes retries idempotent.

!Tinder - Deep Dive Diagram.excalidraw

### 5.4 Sharding and storage

- Swipes: Cassandra or DynamoDB keyed by `swiperId` (query "what did I swipe", and it spreads write load), plus an inverted table keyed by `targetId` for "who liked me" (also drives a "likes you" feature). Write-heavy and append-only fits LSM storage.
- Profiles: Postgres, sharded by userId when needed; heavily cached since profile data rarely changes.
- Geo index: sharded by region (city clusters) so a query hits one shard, with replicas for read throughput.

### 5.5 Notifications

Match events go through a queue (Kafka/SQS) to the Notification Service. It sends a push through APNs/FCM and, if the user has a live WebSocket, pushes in-app immediately. The in-app badge is derived from the match table, so a lost push is only a delay, never a lost match.

### 5.6 Failure modes and abuse

- **Hot users** (very popular profiles) collect many pending likes: cap the in-memory window per user and keep older ones in the store.
- **Redis loss:** rebuild Bloom filters and pending-like state from the swipe store; meanwhile fall back to direct store reads.
- **Bots and spam swiping:** per-user rate limits, anomaly detection on swipe rate and like ratio.
- **Privacy:** never return exact coordinates; return rounded distance and compute it server side. Blocked and deleted users are filtered at query time.

## 6. What interviewers look for

- **Mid-level:** correct APIs and data model; a working design covering feed, swipes and matching; handles geo filtering and avoiding duplicate profiles at a basic level (a swipe store, mutual-like check, notification).
- **Senior:** proactively discusses feed efficiency and scale: a real geo index (Elasticsearch / geohash), precompute plus fallback, cache staleness, Bloom filter trade-offs, the simultaneous-swipe race and atomic or idempotent match creation, honest capacity numbers.
- **Staff+:** deep, experience-backed choices and anticipates problems: Redis Lua vs single-partition Cassandra transactions, sizing and tuning the Bloom false-positive rate, adaptive geo sharding for dense cities, TTL and invalidation strategy for precomputed stacks, failure rebuilds from the durable store.

## 7. Common pitfalls

- Full table scans or per-request distance math over all users
- Computing "seen" by joining swipes at query time without a bounded structure
- Checking for the reverse swipe before writing your own (race loses matches)
- Creating duplicate matches or duplicate notifications on retries
- Indexing every user's location in real time
- Putting photos in the database or the API path
