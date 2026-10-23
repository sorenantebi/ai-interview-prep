---
topic: "Search & Analytics"
difficulty: Hard
problem: "YouTube Top K"
---
# Design YouTube Top K Videos – Solution

**Topic:** Search & Analytics · **Difficulty:** Hard · **Question:** YouTube Top K - Question

## 1. Requirements

**Functional**
- Query the top K videos (K up to 1,000) by view count
- Windows: all time, last hour, last day, last month. Treat them as **tumbling** windows (aligned to the hour/day/month), and treat sliding windows as an extension (5.5)
- Results must be **precise**, not approximate (approximation is a deep dive, 5.6)

**Non-functional**
- ~1 minute of delay between a view and it showing up in the results is acceptable
- Query latency of ~10 ms
- Very high write throughput: ~70B views/day ≈ **~700K views/s**

**Out of scope:** personalisation, bot/fraud filtering (an upstream stage), per-category or per-region boards (add the category to the key).

## 2. Back-of-envelope

- Videos: ~1M new/day × 10 years ≈ **3.6B videos**. A `(videoId, count)` row of ~18 B gives **~64 GB** for the all-time table: it fits on one big machine's disk but not comfortably in one DB's write capacity.
- Writes: 700K/s ÷ ~10K writes/s per Postgres instance ≈ **~70 shards** if every view is a write. Batching (5.2) cuts this to about 5-10 shards.
- Reads: the answer is K × ~50 B ≈ 50 KB and changes once a minute, so it is a caching problem, not a database problem.
- Window tables multiply storage (one row per video per hour). That is why we pre-aggregate (5.3).

## 3. Core entities and API

Entities: `Video`, `View` (an event), `TimeWindow`.

```
GET /views/top-k?window={all|hour|day|month}&k={K}   ->  [ { videoId, views } ]
```

View events do not need a public API: they come from the existing View Service (the player/CDN logs) into Kafka.

## 4. High-level design

!YouTube Top K - Diagram.excalidraw

Build it in two phases, as you would at a whiteboard:

1. **All-time top K.** View events go into **Kafka partitioned by `videoId`**, a consumer increments counts in **Postgres with an index on `views`**, and the query is `ORDER BY views DESC LIMIT k`. The index makes it O(k). The bottleneck is write volume on one database.
2. **Time windows.** Add an hour-grain timestamp so there is one row per (video, hour). Windowed queries now have to scan and sum a huge number of rows, which is too slow and multiplies storage.

The sections below fix those two problems. The final shape is: **Kafka -> Flink (batch/aggregate) -> sharded Postgres with pre-aggregated window tables -> Redis cache refreshed by a cron job -> Top-K Service**.

## 5. Deep dives

### 5.1 Reducing database query load (the read path)

| Approach | Verdict | Notes |
|---|---|---|
| Query the DB per request | Bad | Even with an index, windowed queries are expensive at high read QPS |
| **Cache** top-K per window in Redis/Memcached (TTL ~2 h) | Good | Sub-ms hits. A miss after expiry runs the heavy query and breaks the 10 ms SLA |
| **Precompute with a cron job** before the TTL expires | Great | Cache is always warm, so latency is predictable. Cost: operational complexity, and the job needs monitoring and alerting if it fails |

A CDN or API-gateway cache in front (30-60 s) removes nearly all read QPS, since K ≤ 1,000 and the answer changes only about once a minute.

### 5.2 Handling 700K writes/s

- **Shard** Postgres by `videoId`, aligned with the Kafka partitions (~70 shards at ~10K writes/s each). Top-K then needs a **merge across shards**.
- **Batch with Flink** before writing: a 1-hour tumbling window per video with a bounded-out-of-orderness watermark (about 30 s for late events) turns many view events into one upsert per video per window. That reduces write volume by 2-100× (depending on how skewed popularity is) and lets you run **~5-10 shards**. Flink checkpoints state and Kafka offsets, so it recovers without double counting.
- **Why merging partition-local top-Ks is exact:** because Kafka is keyed by `videoId`, all views of a video land in one partition, so each partition holds *exact* counts for its videos. The global top K is guaranteed to be inside the union of each partition's local top K, so a merge of `P × K` items gives the right answer.
- **Hot videos:** pre-aggregate locally (emit `(videoId, +137)` per second, not 137 events). If one key is still too hot, salt it and re-merge.

### 5.3 Optimising windowed queries

| Approach | Verdict | Notes |
|---|---|---|
| Scan hour rows and sum for the requested window | Bad | Scans billions of rows |
| **Aggregate at coarser grains** (hour -> day -> month tables) | Good | Fewer rows to scan for long windows. Adds write load and some lag from rolling up |
| **Pre-aggregated window tables** (`VideoViewsLastHour`, `...LastDay`, `...LastMonth`), each indexed on views | Great | Each window query is as fast as the all-time one. Cost: ~4 tables updated per batch, and bulk updates get more complex |
| **In-memory aggregation in Flink** (RocksDB-backed state, writing straight to the cache) | Great (complex) | Removes the DB as a bottleneck. Requires real Flink expertise and invites low-level questions |

**Recommended:** Flink batching -> sharded Postgres with pre-aggregated window tables -> Redis cache refreshed by cron -> Top-K Service. It meets 700K writes/s, ~10 ms reads and ~1 minute of staleness.

### 5.4 Fault tolerance and correctness

- Flink state (RocksDB) is checkpointed to object storage with the Kafka offsets, so a restart replays from the last offset. Sinks upsert by `(window, videoId)`, so the processing is idempotent.
- Duplicate views from client retries are filtered with an event ID, or tolerated, since the leaderboard is not billing-grade.
- A batch job (Spark over raw events archived in S3) can recompute exact numbers for completed hours/days and overwrite streaming results. This corrects drift and very late events (the Lambda-style safety net).
- If Redis is lost, the cron job rebuilds the cache on its next run (about a minute).

### 5.5 Sliding windows

!YouTube Top K - Deep Dive Diagram.excalidraw

- Batch at **minute grain** instead of hour grain, and keep the counts per `(videoId, minute)`.
- "Last hour" = last 60 minute buckets. Maintain it incrementally: `hourCount += newMinute - expiredMinute`. When the window slides, read the minute that expired (T-60), subtract it, add minute T, and update the window tables with the difference.
- Alternative: two Kafka consumer groups on the same topic, one incrementing immediately and one decrementing after a 60-minute lag.
- The cost is memory in Flink: roughly **43,200× more state** for minute-level sliding windows over a month, so push the long windows (day, month) to rolled-up hour/day buckets.
- Keeping only the top N (about 10×K) per bucket bounds memory at the price of a small error for long-tail videos; the batch job corrects this.

### 5.6 Approximation with Count-Min Sketch (when exactness is relaxed)

| Approach | Verdict | Notes |
|---|---|---|
| Redis **Count-Min Sketch** + sorted set trimmed to 1,000 | Good | Counts in hundreds of MB instead of ~64 GB. Risk: a view can be added to the sketch but not the sorted set after a crash |
| **Flink + CMS** with the sorted list in checkpointed state | Great | Replay from Kafka offsets on failure, with no durability gap. Needs Flink expertise |

A CMS only overestimates (error ≤ ε·N with probability 1-δ), and it cannot enumerate keys, so it needs a heap alongside it. Space-Saving / Misra-Gries is a good fit for small K. Since the requirement is **precise** results, CMS is the answer to "what if exactness were relaxed to save memory?", not the default.

### 5.7 Specialised databases

- **InfluxDB / Prometheus: bad.** Billions of distinct `videoId`s is a cardinality problem for them, and scan-heavy `top()` queries fail.
- **TimescaleDB: good.** Postgres with hypertables and **continuous aggregates** for last-hour/day/month roll-ups, partitioned by `videoId`. It still needs caching and sharding to hit the SLA.
- **Real-time OLAP (Druid, Pinot, ClickHouse): good.** Druid rolls up at ingestion by minute + `videoId` and compacts to coarser grains, Pinot uses star-tree indexes and pre-aggregated segments, and ClickHouse uses materialized views into SummingMergeTree/AggregatingMergeTree for minute/hour/day roll-ups. The trade-off is production complexity (compaction, node outages) at this scale.

## 6. What interviewers look for

- **Mid-level:** a working end-to-end design (Kafka, a counter store, an index for top K, a cache), roughly 80% breadth and 20% depth. Sees some bottlenecks (write volume, window queries) and may not solve them all.
- **Senior:** a near-optimal design at about 60% breadth and 40% depth. Proactively finds the write bottleneck and fixes it with sharding and Flink batching, designs pre-aggregated window tables, protects the 10 ms SLA with a precomputed cache, and states trade-offs with confidence.
- **Staff+:** about 40% breadth and 60% depth. Anticipates problems before they appear, and compares the alternatives (Flink state, CMS, TimescaleDB, Druid/Pinot/ClickHouse, sliding vs tumbling windows) with judgement and operational experience. The interviewer steers for focus, not direction.

## 7. Common pitfalls

- Sorting all videos on every request, or running `COUNT(*) GROUP BY` on a raw views table
- Writing one DB update per view (hot-row contention, ~700K writes/s)
- Partitioning by anything other than `videoId`, which breaks the exactness of merging local top-Ks
- Scanning hour rows for month windows instead of pre-aggregating
- Letting a cache entry expire under load (a stampede on the heavy query) instead of precomputing
- Reaching for a time-series DB such as InfluxDB without checking cardinality
