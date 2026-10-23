---
topic: "Messaging & Real-time"
difficulty: Hard
problem: "FB Live Comments"
---
# Design FB Live Comments (Live Video Comment Stream) – Solution

**Topic:** Messaging & Real-time · **Difficulty:** Hard · **Question:** FB Live Comments - Question

## 1. Requirements

**Functional**
- Viewers post comments on a live video
- Viewers see new comments from others in near real time while watching
- A viewer joining mid-stream sees the comments posted before they joined (most recent first) and can page back through older ones

**Non-functional**
- Scale: millions of concurrent videos, thousands of comments/s on a single popular stream, up to ~1M+ viewers on one video
- **Availability over consistency;** eventual consistency is fine. Viewers may see comments in slightly different order; a dropped comment on a busy stream is tolerable, a lost *stored* comment less so
- Low latency: **< 200 ms** end to end (the threshold where humans perceive "live"); relaxed to ~1-2 s only for mega-streams (5.3)
- Massive read fan-out: one comment is delivered to up to ~1M viewers; a hot video must not hurt others

**Out of scope:** the video pipeline, reply threads, reactions, comment ranking, security and content moderation, ads.

## 2. Back-of-envelope

- Hot stream: 1M viewers, 5K comments/s, naive delivery = 5K x 1M = **5B messages/s**. Impossible, and also unreadable (a human reads ~5-10 comments/s). Hence the design must **sample, batch or snapshot on the delivery side**.
- Sensible target per viewer: <= ~10-20 comments/s delivered, in batches.
- Connections: ~100K+ per server, so a 1M-viewer stream needs ~10+ servers; ~10M concurrent viewers overall means ~100+ servers.
- Storage: 1 comment ~ 200 B; 1B comments/day ~ 200 GB/day, ~70 TB/year. Easy for a wide-column store.

## 3. Core entities and API

Entities: `User` (broadcaster or viewer), `LiveVideo` (owned by another team's system), `Comment { liveVideoId, commentId, userId, text, ts }`.

```
POST /comments/:liveVideoId   { text }                 (userId from the auth header)  -> 201 { commentId }
GET  /comments/:liveVideoId?cursor={commentId}&pageSize=10&sort=desc   -> older comments (paging)
GET  /comments/:liveVideoId/stream   (SSE)   <- new comments, resumes via Last-Event-ID
```

`commentId` is a time-ordered id (snowflake/ULID): a natural cursor for paging and for `Last-Event-ID` resume.

## 4. High-level design

!FB Live Comments - Diagram.excalidraw

Baseline: commenter client -> **Comment Management Service** -> **Comments DB** (DynamoDB-style); viewers fetch via the GET endpoint. Polling the DB for new comments is the naive first cut and breaks down quickly (5.1). The real design adds **Realtime Messaging Servers** for push:

- **Write path:** the Comment Management Service validates, rate-limits, persists to the comments DB, and publishes the comment to the pub/sub channel for its `liveVideoId`.
- **Delivery path:** viewers hold an SSE connection to a realtime messaging server, reached through an L7 load balancer that routes by `liveVideoId`. The server subscribes to a video's channel only if it has local viewers of that video, and relays comments to them.
- **Join path:** on connect, the server returns the last N comments from a Redis list, then switches to the live stream. Older pages come from the DB through the GET endpoint.

## 5. Deep dives

### 5.1 Real-time broadcasting: polling vs WebSocket vs SSE

| Option | Verdict |
|---|---|
| Short polling | **Bad.** 1M viewers x 1 req/s = 1M RPS of mostly empty responses against the DB; latency up to the poll interval, cannot hit < 200 ms |
| Long polling | Works everywhere, but a new request per batch, heavy headers, reconnect churn |
| WebSocket | **Good.** Bidirectional, low latency, but stateful and wasteful here because the traffic is read-heavy and writes are rare |
| **SSE (Server-Sent Events)** | **Great.** A persistent one-way push over plain HTTP, built-in auto-reconnect with `Last-Event-ID`, cheap; fits the read/write imbalance (comments are posted through ordinary HTTPS POST) |

WebSocket is acceptable if you justify it explicitly.

### 5.2 Scaling to millions of concurrent viewers: pub/sub across servers

The coordination problem: viewers of one video are spread over many servers, so a comment arriving at one server must reach all of them.

| Approach | Notes |
|---|---|
| Naive pub/sub (**Good**) | Every server subscribes to every video's channel. Works, but each server is flooded with comments for videos none of its viewers watch |
| **Partitioned pub/sub + L7 LB with consistent hashing on `liveVideoId`** (**Great**) | Hash video ids onto N channels/partitions; the L7 load balancer sends viewers of the same video to the same small set of servers, so a server subscribes only to channels it needs. Little wasted traffic |
| Dispatcher service (alternative) | A service tracks which servers serve which videos and pushes each comment straight to just those servers. No subscriptions to manage, but it is another stateful component to scale and keep consistent |

Pub/sub tech: Redis Pub/Sub channel per video is simple and fast, fire-and-forget (fine for a lossy live feed). Kafka by `liveVideoId` is durable but a hot video lands on one partition. Direct push needs a registry of servers per video.

Co-locating a video on one server hits the 100K-connection limit for a big video: spread a hot video over several servers (hash `liveVideoId` plus a bucket), each subscribing to the same channel.

### 5.3 Mega-streams (5,000+ comments/s)

At this rate nobody can read every comment, so degrade on the delivery side. All comments are still stored.
- **Good: sample by velocity.** Above a threshold (~20/s per viewer) drop the lowest-ranked comments (non-friends, low reputation) before sending; batch flushes every 250-500 ms.
- **Great: CDN snapshots.** The server keeps a buffer of the latest comments and snapshots it about every second to the CDN; viewers poll the CDN instead of holding SSE connections. Adds 1-2 s latency, which is acceptable since individual comments scroll by too fast to read anyway, and it offloads connection handling entirely.
- A two-tier tree (publisher -> regional relay -> servers) keeps cross-region bandwidth bounded.

### 5.4 Disconnections and missed comments

- **Bad:** ignore it; viewers silently lose comments.
- **Great:** SSE reconnects automatically and sends `Last-Event-ID`; the server replays the missed comments from the Redis recent list (or DB). The client tracks its position locally and shows a graceful catch-up. Use **bounded replay** (e.g. last ~5 minutes) so a long absence does not flood the client; gaps beyond that are ignored (it is live content).
- Reconnect with jittered backoff to avoid a reconnect storm after a server dies.

### 5.5 Storage, history and ordering

- Access pattern: append by video, read by `(liveVideoId, time range)` newest first. Use **DynamoDB/Cassandra**, partition key `liveVideoId` (+ time bucket such as `liveVideoId#hour` to avoid unbounded hot partitions), sort key `commentId DESC`.
- Recent comments (last ~100-500) are kept in a Redis list per video, trimmed on write, so a joining viewer rarely touches the DB.
- Writes may go through a Kafka buffer (partitioned by `liveVideoId`) with a batch consumer, so a DB slowdown never delays live delivery: delivery rides pub/sub, persistence rides the queue.
- No global order needed: use the time-ordered `commentId`; clients sort the small window they hold. The poster sees their own comment immediately (optimistic insert), then reconciles.
- After the stream ends, comments are kept as part of the replay; cold ones tier to cheaper storage.

### 5.6 Failure modes and abuse

- **Realtime server death:** SSE auto-reconnects via the LB to another server, which re-subscribes.
- **Pub/sub node down:** comments pause for that shard until failover; persisted comments are unaffected (separate write path).
- **Slow consumers:** bounded per-viewer buffer, drop oldest rather than grow memory.
- **Spam/abuse** (out of scope in the interview, but worth a sentence): per-user rate limit, async moderation, tombstone events for removed comments.
- **Celebrity goes live:** pre-warm servers, autoscale on connection count, not CPU.

## 6. What interviewers look for

- **Mid-level (more breadth than depth):** recognize that polling does not scale, propose a push model (SSE or WebSocket) with pub/sub between servers, understand each component and the schema; some interviewer guidance expected.
- **Senior (more depth):** quickly produce the high-level design, then spend time on scaling: proactively spot the limits of simple pub/sub and propose partitioning/consistent hashing, SSE vs WebSocket reasoning, separate delivery and persistence paths, reconnect/backfill semantics, trade-offs; little steering needed.
- **Staff+ (mostly depth):** breeze through basics, anticipate reliability and scalability issues on their own, name concrete technologies from experience, and bring up mega-streams, sampling and CDN snapshots unprompted (including the latency trade-off).

## 7. Common pitfalls

- Opening one WebSocket per viewer *and* publishing per viewer from the API
- Every server subscribing to every video channel
- Ignoring that one hot video concentrates all load on one partition, channel or server
- Treating it like a chat system with strict delivery and ordering guarantees
- Writing every comment synchronously in the delivery path
- Forgetting how a late joiner or a reconnecting viewer gets missed comments
