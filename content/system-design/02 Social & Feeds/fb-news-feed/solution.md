---
topic: "Social & Feeds"
difficulty: Medium
problem: "FB News Feed"
---
# Design Facebook News Feed – Solution

**Topic:** Social & Feeds · **Difficulty:** Medium · **Question:** FB News Feed - Question

## 1. Requirements

**Functional**
- Create a post (text plus media reference)
- Follow another user (one-directional relationship; unfollow is the symmetric delete)
- View a feed of recent posts from followed accounts in reverse chronological order (newest first)
- Page through the feed (infinite scroll)

**Non-functional**
- **Availability over consistency**: a new post may take up to ~1 minute to show up in followers' feeds (a few seconds is typical)
- Post creation and feed load both < 500 ms (p99)
- Scale: 2B total users (~500M DAU) and effectively unlimited follows per user, including accounts with tens of millions of followers

**Out of scope:** likes/comments, visibility and privacy restrictions, ad insertion, the ML ranking model itself (we only show where it plugs in), media upload (see Instagram - Solution).

## 2. Back-of-envelope

- Feed reads: 500M × 10 = 5B/day ≈ **58K/s average, ~200K/s peak**
- Posts: 200M/day ≈ **2.3K writes/s**. Reads outnumber writes by roughly 25:1.
- Fan-out on write: 200M posts × ~200 followers = 40B feed inserts/day ≈ **460K inserts/s**. This is the real write load, and it is 200x the post rate.
- Feed cache: keep the latest ~500 post ids per active user, 8 B each ≈ 4 KB. 500M users × 4 KB ≈ **2 TB of Redis**, which is a modest cluster.
- Post store: ~1 KB metadata per post × 200M/day × 365 × 5 years ≈ **~365 TB**. Media lives in blob storage and a CDN, not here.

## 3. Core entities and API

Entities: `User`, `Follow { followerId, followeeId }` (directed edge), `Post { postId, authorId, content, createdAt }`. Internal only: the precomputed feed list per user (`userId -> [postId]`).

```
POST /posts                              { content }                     -> { postId }
PUT  /users/{id}/follow                                                  -> 204
GET  /feed?pageSize=20&cursor={cursor}                                   -> { items: Post[], nextCursor }
```

The cursor is the timestamp (or time-sortable `postId`, Snowflake style) of the oldest post the client has seen, so the next page is "older than the cursor". The caller's user id comes from the auth token, never from the request body.

**Baseline design (before optimising):** Post Service writes to a key-value store (DynamoDB). The Follow table is keyed by follower with a **global secondary index** on followee (so "who follows X" is cheap), and the Post table is keyed by `authorId` with `createdAt` as sort key. A naive Feed Service queries the Follow table, then each followee's recent posts, and merges. This works but is exactly the fan-out on read that the deep dives fix.

## 4. High-level design

!FB News Feed - Diagram.excalidraw

- **Follow path:** Follow Service writes the edge to the Follow table (with its follower-lookup index).
- **Write path:** Post Service stores the post, then publishes a `post-created` event to a queue (SQS or Kafka). Fan-out workers look up the author's followers in the Follow table and push the `postId` into each follower's feed list in Redis.
- **Read path:** Feed Service reads the precomputed list of ids from Redis, **hydrates** them into full posts (batch multi-get from a post cache / Post Store plus author profile and counters), optionally re-ranks, and returns a page.
- Feed Cache holds only ids, which is cheap and avoids copying post bodies into every follower's list. Edits and deletions then touch one record.

## 5. Deep dives

The three core problems: (a) users who follow many accounts, (b) accounts with many followers, (c) a few posts that are read far more than the rest. 5.1 covers (a) and (b); 5.7 covers (c).

### 5.1 Fan-out on read vs write vs hybrid

| Approach | How | Pros | Cons |
|---|---|---|---|
| Fan-out on read (pull), a bad solution | At read time, fetch the last posts of all N followees, merge and sort | No write amplification, always fresh, no storage for feeds | N parallel lookups on every read (N ~ 200+), slow tail latency, expensive at 200K reads/s |
| Fan-out on write (push), a good solution | At post time, insert postId into every follower's feed (fixed-size list per user, e.g. 200 ids) | Reads are one cache lookup, very fast; storage is small (~2 KB per user, ~4 TB for 2B users) | 10M followers = 10M inserts per post, wasted work for inactive users |
| **Hybrid**, the great solution | Push for normal accounts, pull for celebrities, merged at read time | Cheap reads and bounded write cost | Two code paths, merge logic |

**Recommended: hybrid.** Mark accounts above a follower threshold (e.g. 10K to 100K) as celebrities. Their posts are *not* fanned out. At read time Feed Service takes the precomputed list and merges in recent posts from the celebrities the user follows (a small set, looked up from an author index in the Post Store, with a hot cache). Also skip fan-out to users inactive for 30+ days and rebuild their feed lazily on next login (cold start from pull).

!FB News Feed - Deep Dive Diagram.excalidraw

#### Handling accounts with many followers (the write side)

- **Bad:** the Post Service synchronously inserts into every follower's feed inside the request: bursty, uneven load and slow posts.
- **Good:** put the fan-out behind a queue; async workers consume `post-created` events and update feeds, which is fine because ~1 minute of staleness is allowed. Scale workers on consumer lag.
- **Great:** hybrid on top of the queue: exclude accounts above the follower threshold from fan-out entirely and merge their posts at read time.

### 5.2 Feed cache layout

- Redis list or sorted set per user: `feed:{userId} -> [postId...]`, capped at ~500 entries (`LPUSH` + `LTRIM`). Sorted set with the time-sortable id as score supports cursor reads (`ZREVRANGEBYSCORE`).
- Entries beyond the cap are served by a slower fallback that rebuilds from pull; very few users scroll that deep.
- Shard by `userId` (consistent hashing). Replicas for availability. Losing a shard is survivable because the feed can be rebuilt from the Post Store and graph.

### 5.3 Pagination

Use **cursor-based** pagination: the cursor is the timestamp / last postId (or score) returned, i.e. the oldest item already shown. Offset pagination breaks because new posts shift positions, causing duplicates and gaps. The client also polls or receives a push for "new posts available" instead of silently inserting at the top.

### 5.4 Ranking

Chronological order is trivial. For ranked feeds, a **candidate generation** stage (the merged ~500 ids) feeds a **scoring** stage (lightweight model on features like affinity, recency, engagement, post type), run in Feed Service with features from a feature store. Keep the model cheap (a few ms) and precompute affinity offline. Keep the cache chronological; ranking happens on read so models can change without rewriting feeds.

### 5.5 Storage choices

| Data | Store | Why |
|---|---|---|
| Posts | Cassandra / DynamoDB, key `postId`, plus index by `authorId, time` | Write heavy, key-value, horizontal scale |
| Social graph | Sharded MySQL/Postgres or a graph-ish KV (both directions: followers and followees) | Need fast follower enumeration for fan-out and followee list for pull |
| Feeds | Redis | Latency, list/zset semantics |
| Media | S3 + CDN | Not in the feed path; posts carry URLs only |

### 5.6 Failure modes and operations

- **Fan-out lag:** Kafka partitions keyed by authorId; scale workers on consumer lag. Posts appear late but nothing is lost. Idempotent inserts (zset by postId) make retries safe.
- **Hot keys:** celebrity profile reads cached in a local in-process cache plus Redis; stagger TTLs to avoid stampedes.
- **Deleted/blocked content:** filter at hydration time (tombstone check) rather than removing from millions of lists.
- **Redis down:** serve from pull path with degraded latency, or return a slightly stale feed from a replica.
- **Unfollow:** filter by current follow set on read, and lazily clean entries.

### 5.7 Uneven post reads (viral posts)

Hydration reads post bodies by id, and a viral post is read by millions of feeds at once.

- **Good:** a distributed post cache (Redis keyed by `postId`, LRU plus TTL) in front of the Post Store. Weakness: the **hot key** problem, since one shard owns the viral post and becomes the bottleneck.
- **Great:** **replicate** the hot entries so any cache instance can serve any post, with a load balancer spreading reads. It spends cache capacity to buy throughput. In practice combine it with a small in-process cache on the Feed Service for the very hottest ids, and a CDN for media.

## 6. What interviewers look for

- **Mid-level:** correct entities, APIs and data model, a working design (Follow table with a follower index, posts by author and time, timestamp cursor). Notices that reading from many followees does not scale, with the interviewer driving the fixes.
- **Senior:** quickly covers the basics, then goes deep on 2+ problems: precomputed feeds, async fan-out through a queue, hybrid with a celebrity threshold, numbers for write amplification, inactive users, hydration, ranking placement. Articulates trade-offs and surfaces the fan-out problem unprompted.
- **Staff+:** covers all three deep dives (many followees, many followers, hot posts) with little steering and shows hands-on judgement: threshold tuning, replicated hot-post caches, backpressure and failure handling, rebuild of lost feeds, and how ranking evolves without rewriting stored feeds.

## 7. Common pitfalls

- Doing a SQL join across all followees on every feed request
- Fanning out synchronously inside the post request
- Ignoring the celebrity problem or treating it as an afterthought
- Storing full post bodies in every follower's feed
- Offset-based pagination on a feed that keeps changing
- Mixing ranking logic into the write path so models cannot evolve
