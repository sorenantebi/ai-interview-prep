---
topic: "Social & Feeds"
difficulty: Medium
problem: "Strava"
---
# Design Strava – Solution

**Topic:** Social & Feeds · **Difficulty:** Medium · **Question:** Strava - Question

## 1. Requirements

**Functional**
- Record an activity on a device (offline-capable) and upload it afterward
- View an activity: map, distance, pace, elevation, heart rate
- Follow athletes and view a feed of their activities
- Automatic segment matching and per-segment leaderboards (overall, friends, time period)

**Non-functional**
- Uploads must be durable and resumable; a recorded run must never be lost
- Stats visible quickly (seconds), segment results within about a minute (async is fine)
- Feed < 300 ms, leaderboard reads < 100 ms
- Scale: ~5M activities/day, read heavy for feed and leaderboards

**Out of scope:** live tracking (mention as an extension), routes and heatmaps, training analytics, payments.

## 2. Back-of-envelope

- Uploads: 5M/day ≈ **58/s average**, a few hundred/s at weekend morning peaks.
- Raw GPS: 3,600 points × ~30 B ≈ 100 KB (about 30 KB compressed in FIT/GPX or encoded polyline). 5M × 100 KB ≈ **500 GB/day, ~180 TB/year**. Blob storage, with older raw streams tiered to cold storage.
- Metadata and stats: ~2 KB/activity → 10 GB/day, trivial.
- Segment matching: an activity of 3,600 points covering ~20 S2 cells touches maybe 20 to 200 candidate segments. 58 activities/s × ~100 candidates = ~6K cheap candidate checks/s, easy for a worker pool.
- Reads: 50M DAU × ~5 feed loads = 250M/day ≈ **3K/s**, leaderboards a similar order. Cached for most.

## 3. Core entities and API

Entities: `Athlete`, `Follow`, `Activity { activityId, athleteId, type, startTime, distance, movingTime, elevation, status, visibility }`, `Segment { segmentId, polyline, startPoint, endPoint, length }`, `Effort { activityId, segmentId, athleteId, elapsedSeconds, startIndex }`.

```
POST /activities                    { type, startTime, sizeBytes, idempotencyKey } -> { activityId, uploadUrls[] }
POST /activities/{id}/complete                                                     -> 202
GET  /feed?cursor=&limit=                                                          -> { activities[], nextCursor }
GET  /segments/{id}/leaderboard?scope=overall|friends|year&limit=50                -> { entries[], myRank }
```

The client uses an idempotency key (a UUID generated on device) so retried uploads after a network drop never create duplicates.

## 4. High-level design

!Strava - Diagram.excalidraw

- **Upload path:** Activity Service creates a `PENDING` row and returns presigned URLs. The device uploads the GPS file (chunked, resumable) straight to S3. On completion an `activity-uploaded` event goes to Kafka.
- **Processing:** workers read the file, compute stats (distance, moving time, elevation with smoothing and DEM correction), find matching segments, write efforts, update leaderboards, and flip the activity to `DONE`.
- **Read path:** Feed Service reads followed athletes' activities and leaderboard queries hit Redis. The upload response is instant; stats appear when processing finishes (usually seconds).

## 5. Deep dives

### 5.1 Reliable upload

Phones record to local storage while offline, and the app uploads when connectivity returns. Use presigned multipart upload so a dropped connection resumes from the last part. The activity file is immutable once uploaded. Keep the original so improved algorithms can be rerun later (see 5.5).

### 5.2 Segment matching

Comparing each activity to tens of millions of segments is impossible. Use a **spatial index**:

| Option | How | Pros | Cons |
|---|---|---|---|
| Brute force over all segments | Distance check per segment | Trivial | Infeasible at this scale |
| PostGIS R-tree | `ST_Intersects` on a geometry column | Exact, flexible | Heavy per-activity queries, harder to scale horizontally |
| **S2/geohash cell index** | Each segment is indexed under the cells (level ~16, a few hundred meters) it passes through; key `cell -> segmentIds` | O(cells) lookup, shardable by cell, cacheable | Needs a precise second stage |

Pipeline: (1) convert the activity track into the set of cells it crosses, (2) fetch candidate segments for those cells in a batch lookup, (3) **verify** each candidate: the track must pass within a tolerance (e.g. 20 to 30 m) of the segment start, follow its polyline in order and direction, and reach the end, then compute elapsed time by interpolating timestamps between points at start and end, (4) write the effort.

!Strava - Deep Dive Diagram.excalidraw

### 5.3 Leaderboards

- **Per segment Redis sorted set**, member = `athleteId`, score = best elapsed time. On a new effort do `ZADD ... LT` (update only if lower) for a personal record. Top-N is `ZRANGE`, "around me" is `ZRANK` then a range window, and friends view is `ZMSCORE` over the athlete's followee ids (or a pre-filtered sorted set merge capped to a sane friend count).
- Time-bucketed sets (`seg:{id}:2026`, `:month`) support "this year" / "this month" and age-group filters without scanning all efforts.
- Durability: the **Efforts DB** (Cassandra/Postgres, partition by `segmentId`) is the source of truth, Redis is a derived index that can be rebuilt. A very popular segment with 1M+ members is still only tens of MB, so it fits easily.
- Ranks are eventually consistent: a new effort shows up within seconds.

### 5.4 Activity feed

Same shape as FB News Feed - Solution but gentler: athletes follow ~100 others on average and post about 1 activity/day, so write amplification is small. **Fan-out on write** into a per-athlete Redis list of activityIds is fine for ordinary users, with pull-based handling for the few accounts with huge follower counts. Respect visibility (private, followers-only, hidden start/end zone) at read time. Feed items carry a pre-rendered **static map thumbnail** (generated by a worker, stored on S3/CDN) so the feed never draws maps live.

### 5.5 Idempotency and re-processing

- Processing keys are `activityId`, and effort rows are upserts on `(activityId, segmentId)`, so Kafka's at-least-once delivery cannot duplicate efforts.
- Store an `algorithmVersion` on each result. When matching or elevation logic improves, or a segment is created or edited, a backfill job re-reads the raw GPS from S3 and replays through the same pipeline at low priority, with rate limits to protect Redis and the DB. A newly created segment is back-filled using the cell index to find historic activities in its cells.

### 5.6 Storage choices

| Data | Store | Reason |
|---|---|---|
| Raw GPS streams | S3 (Parquet/FIT), cold tier after a year | Large, write-once |
| Activity metadata, stats | Postgres (sharded by athleteId) or DynamoDB | Moderate volume, queryable by athlete and time |
| Efforts | Cassandra, partition `segmentId`, cluster by time | Write-heavy, queried by segment |
| Segment index | KV store / Redis keyed by cell | Fast candidate lookup |
| Leaderboards, feeds | Redis | Sorted sets and lists |

### 5.7 Failure modes and extensions

- **Poison files** (corrupt GPX, GPS jumps, teleporting): validate and clean (speed sanity checks, outlier removal), mark `FAILED` with a reason, retry bounded, dead-letter queue.
- **Cheating:** cap plausible speeds per activity type, flag e.g. a "ride" at car speeds, and let users report efforts.
- **Live tracking** (beacon): the app streams points over HTTPS/WebSocket to a stateless ingest service into Kafka and a Redis "latest position" key per athlete, which followers poll or subscribe to. Final activity is still saved through the normal upload.
- **Privacy:** hidden zones are removed from the track served to viewers, never from the owner's raw file.

## 6. What interviewers look for

- **Junior:** upload API, DB for activities, feed by querying followees.
- **Mid:** blob storage with presigned uploads, async processing via a queue, sorted-set leaderboards, caching.
- **Senior:** geospatial index for segment candidates plus a verification stage, idempotent and re-runnable pipeline with algorithm versions, derived-vs-source-of-truth for leaderboards, privacy and cheat handling, honest capacity numbers.

## 7. Common pitfalls

- Storing GPS points as one row each in a relational table
- Doing segment matching or stats inside the upload request
- Checking every segment against every activity
- Making Redis the only copy of leaderboard data
- No idempotency key, leading to duplicate activities on retries
- Ignoring privacy zones and visibility in the feed
