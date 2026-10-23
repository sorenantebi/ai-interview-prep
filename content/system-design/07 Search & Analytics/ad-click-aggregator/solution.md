---
topic: "Search & Analytics"
difficulty: Hard
problem: "Ad Click Aggregator"
---
# Design an Ad Click Aggregator – Solution

**Topic:** Search & Analytics · **Difficulty:** Hard · **Question:** Ad Click Aggregator - Question

## 1. Requirements

**Functional**
- A user clicks an ad and is redirected to the advertiser's page, and the click is recorded
- Advertisers query aggregated click metrics (by ad, optionally by campaign/country/device) at a granularity of 1 minute and up

**Non-functional**
- Scale: ~10M active ads, **~10K clicks/s at peak** (~1K/s average, ~100M clicks/day). Design with headroom for ~10x bursts, scalable horizontally
- **Zero data loss** and **idempotent click tracking**: no lost clicks and no double-counted clicks (billing-grade accuracy)
- Sub-second analytics queries, with near-real-time visibility for advertisers (seconds to a minute)
- Fault tolerant, and the raw data is kept so results can be recomputed

**Out of scope:** ad targeting and ad serving/bidding, cross-device tracking, offline marketing integration, impressions pipeline, detailed fraud ML (mention as a filter stage).

## 2. Back-of-envelope

- 1K/s average × 86,400 ≈ **~100M clicks/day**; peak 10K/s. Provision for a further ~10x burst (100K/s).
- Raw event ≈ 100-200 B (clickId, adId, impressionId, userId, ts, ip, userAgent, country). At ~200 B: **~20 GB/day**, ~7 TB/year raw. Keep in S3 (Parquet, compressed ≈ 4x smaller). Batch view: a 5-minute batch is ~3M events ≈ 300 MB (at 100 B).
- Aggregates: a row `(adId, minute)` exists only for ads with clicks. With 10M active ads and ~100M clicks/day that is at most ~100M rows/day and in practice far fewer (tens of millions, a few GB/day). Small for an OLAP store.
- Kafka: 10K msgs/s × 200 B = 2 MB/s (20 MB/s at a 100K/s burst), which is trivial. 20-50 partitions are plenty, and run 3+ brokers for durability. The bottleneck is not bandwidth, it is hot keys and correctness.
- Dedup cache: ~100M impression IDs/day × 16 B ≈ **1.6 GB**, which fits in one small Redis cluster.
- A single hot ad at 10% of traffic = 1K/s (10K/s in a burst) on one key, so that key must not map to one partition/thread.

## 3. Core entities and API

Entities: `Ad { adId, advertiserId, redirectUrl }`, `Impression { impressionId, adId, userId?, ts }` (one per ad instance shown), `Click { clickId, adId, impressionId, userId?, ts, country, device }`, `Metrics (AdMinuteStats) { adId, windowStart, clicks, uniqueUsers? }`.

```
POST /click    { adId, impressionId, sig }  -> 302 Location: advertiserUrl   (records the click)
GET  /metrics?adId=..&start=..&end=..&granularity=minute|hour|day  -> [{ts, clicks}]
```

(If the click comes from a plain link, a `GET /click?...` carries the same parameters; the logic is identical.) `impressionId` is a unique ID created by the Ad Placement Service when the ad instance was served, **HMAC-signed** with a server secret over `(adId, impressionId)`. It is used for dedup and prevents forged clicks.

## 4. High-level design

!Ad Click Aggregator - Diagram.excalidraw

- **Impression path:** when the ad is served, the Ad Placement Service creates the signed `impressionId` and hands it to the client with the ad.
- **Click path:** a load balancer spreads clicks over a horizontally scalable Click Processor (Click Service). It verifies the signature (microseconds), checks Redis for a duplicate `impressionId`, publishes the event to Kafka/Kinesis (sharded by `adId`), records the ID in Redis, and returns the 302 redirect. Redirect latency does not depend on aggregation.
- **Stream path:** Flink reads Kafka, counts per `(adId, 1-minute window)`, and flushes to an **OLAP store** (ClickHouse / Druid / Pinot, or Redshift/Snowflake/BigQuery).
- **Batch path:** Kafka is also archived to S3. A periodic Spark job recomputes exact aggregates from raw data and overwrites the OLAP rows (reconciliation).
- **Query path:** advertisers hit the Query API, which reads only pre-aggregated data.

## 5. Deep dives

### 5.1 Choosing the aggregation architecture (storage and query strategy)

| Approach | Verdict | Pros | Cons |
|---|---|---|---|
| **Bad:** single DB, store raw events and `GROUP BY` on demand (Postgres/ClickHouse scan) | Bad | Simplest, always exact | Write bottleneck at peak, slow aggregations over billions of rows |
| **Good:** batch processing: raw events to Cassandra (write-optimized), periodic Spark job aggregates into the OLAP DB | Good | Cheap, exact | Minutes-to-hours stale; delays cascade during spikes |
| **Great:** real-time stream processing: Click Service -> Kafka/Kinesis -> Flink/Spark Streaming -> OLAP DB | **Recommended** | Seconds-fresh, flush interval is tunable | Late events and bugs make numbers drift, so add reconciliation |
| Stream + batch reconciliation (lambda-style), see 5.2 | Staff+ extension | Fresh numbers now, exact numbers later, raw data permits fixes | Two code paths (mitigate by sharing logic) |

Billing uses the reconciled numbers, and the dashboard uses the stream numbers, until reconciliation replaces them.

### 5.2 Zero data loss and idempotent click tracking

**Zero data loss (stream side)**
- **Stream retention and replication:** Kafka/Kinesis with replication across brokers/AZs (RF 3, `min.insync.replicas=2`) and ~7 days retention, so a failed processor can replay.
- **Producer side:** Click Service publishes with `acks=all` and the idempotent producer enabled. If the publish fails, do not return success silently, so retry or buffer locally.
- **Flink checkpointing:** snapshot operator state and Kafka offsets together to S3, giving exactly-once state updates. Nuance: for 1-minute windows it matters less, since a restart can just replay ≤ 60 s of the retained stream, but it is cheap insurance for larger windows.
- **Sink:** use **idempotent upserts** keyed by `(adId, windowStart)`, or a transactional two-phase-commit sink, so a replay overwrites rather than adds.
- **Raw event archival:** Kafka Connect S3 sink (or Kinesis Firehose) continuously dumps raw events to the data lake.
- **Reconciliation (lambda-style):** a daily Spark job re-aggregates the raw S3 events, compares with the OLAP rows and overwrites discrepancies. This is the final safety net and the Staff+ answer.

**Idempotency (no double counting)**
- *Bad:* dedup by `userId` (one click per user per ad). It requires login, breaks legitimate repeat clicks and retargeting, and does not distinguish impressions.
- *Great (recommended):* **signed impression IDs.** The Ad Placement Service issues a unique ID per ad instance, HMAC-signed over `(adId, impressionId)`. The Click Service verifies the signature (blocks forged clicks) and checks a dedup cache for the `impressionId`.
- **Dedup cache:** distributed Redis cluster (~1.6 GB for 100M IDs/day), `SET NX` with a TTL (~24 h), RDB/AOF persistence and a replica for failover. A Bloom filter works if a rare miss is acceptable.
- **Ordering matters:** *check* the cache, **publish to the stream, then write the ID to the cache**. If we `SET NX` first and the publish then fails, a client retry is wrongly rejected and the click is lost. With publish-first, a crash between the two steps can only cause a duplicate, which the `clickId`/`impressionId` dedup in the batch job removes.
- The robust formulation is at-least-once delivery + idempotent processing, with the batch job as the final safety net.

### 5.3 Windows and late events

- Tumbling **1-minute event-time windows** based on the click timestamp, not arrival time.
- A **watermark** (e.g. 30 s of allowed lateness) closes windows. Events later than that are routed to a side output / correction topic, and the batch job picks them up.
- Output rows are `(adId, windowStart, count)`. Coarser granularities (hour, day) are rolled up in the OLAP store (materialized views), not recomputed from raw.

### 5.4 Scaling to 10K clicks/s and hot ads (skew)

!Ad Click Aggregator - Deep Dive Diagram.excalidraw

Each tier scales horizontally: Click Service behind a load balancer with autoscaling, Kafka/Kinesis partitioned by `adId`, one Flink job/task per partition, and an OLAP store that scales automatically (managed) or is sharded by advertiser (self-managed).

Partitioning by `adId` keeps all clicks of an ad on one consumer, which is a **hot-shard problem** for viral ads. Use **key salting**: partition by `adId:random(0..N-1)` so one ad spreads over N partitions, pre-aggregate locally per salted key, strip the suffix, and merge the N partial counts per `adId` (second shuffle, or merge on write to the OLAP store). Only salt ads flagged hot (or always with small N). Counts are commutative, so ordering does not matter.

### 5.5 Storage and low-latency queries

| Store | Fit |
|---|---|
| Postgres/MySQL | OK at 50M rows/day with partitioning, but weak for many dimensions and high ingest |
| Cassandra/DynamoDB | Great for key lookups `(adId, window)`, poor for arbitrary group-by |
| **ClickHouse / Druid / Pinot** | Columnar, built for time-series group-by with pre-aggregation; chosen |

Partition by day, order by `(adId, windowStart)`, and keep only aggregates here. Raw data lives in S3 and is queried with Athena/Spark for ad-hoc work. Add a short cache (Redis, 10-30 s) on the Query API for popular dashboards.

**Low-latency queries:** advertisers read only **pre-aggregated** minute rows, which gives a sub-second baseline. For long ranges, nightly jobs (or materialized views) build hour/day/week tables, and a query uses the coarser table for the bulk of the range and drills into finer granularity only at the edges. This trades storage for query speed on the common access patterns.

### 5.6 Failure modes

- **Flink job crash:** it restarts from the last checkpoint, and the sink is idempotent.
- **Kafka broker loss:** replication factor 3, `min.insync.replicas=2`.
- **Redis dedup down:** fail open (accept and dedupe later in the batch job via `clickId`) rather than blocking redirects.
- **Bad deployment of the aggregation logic:** replay from Kafka/S3 into a fresh table and swap.
- **Fraud:** a filter stage in Flink (rate per IP, known bot UAs) tags suspicious events. Keep them in raw but exclude them from billable counts.

## 6. What interviewers look for

- **Mid-level:** the need for pre-aggregation; a working batch design (Spark + separate analytics DB); reasonable answers to idempotency and DB-choice probes. Mostly breadth.
- **Senior:** contrasts batch vs real-time stream processing with trade-offs, finds bottlenecks proactively (hot shards, cascading latency), exactly-once reasoning, late data and watermarks, and goes deep on one or two deep dives.
- **Staff+:** the complete stream + batch reconciliation design (retention, checkpoints, S3 archive, daily re-aggregation), signed impression IDs, hot-key salting, cost and retention, confident technology choices backed by real-world experience; drives the discussion and teaches the interviewer something.

## 7. Common pitfalls

- Incrementing a counter row in a relational DB on every click (write hotspot, no replay)
- Aggregating by processing time, so retries and late events shift minutes
- Claiming "exactly-once" without saying how the sink achieves it
- Ignoring skew from a single viral ad
- Not keeping raw events, which makes bugs unfixable
