---
topic: "Search & Analytics"
difficulty: Hard
problem: "Metrics Monitoring"
---
# Design a Metrics Monitoring Platform – Solution

**Topic:** Search & Analytics · **Difficulty:** Hard · **Question:** Metrics Monitoring - Question

## 1. Requirements

**Functional**
- Collect metrics from hosts and services (name, labels/tags, value, timestamp)
- Query time series with label filters, aggregation (sum, avg, percentiles) and group-by over arbitrary ranges
- Dashboards (graphs, auto-refresh)
- Alert rules (e.g. "error rate > 5% for 5 min") with notification routing (pager, Slack, email)

**Non-functional**
- ~1M samples/s ingest, ~10M active series, linear horizontal scale
- Dashboard queries ~1 s for typical ranges, alert latency within ~1 minute
- Very high write availability: losing the monitoring system during an outage is the worst case. Slightly stale reads are fine.
- Retention: raw 10 s for ~15–30 days, 1-min rollups for ~1 year, 1-hour rollups for years

**Out of scope:** logs and traces (mention as sibling pillars), anomaly-detection ML, billing.

## 2. Back-of-envelope

- 100K hosts × 100 metrics = **10M series**, 10 s interval → **1M samples/s**, 86B samples/day.
- A raw sample is 16 B (8 B timestamp + 8 B double) → 1.4 TB/day uncompressed. With **delta-of-delta timestamps and XOR floats (Gorilla)**, a sample averages ~1.4 B → **~120 GB/day**. 30 days of raw ≈ 3.6 TB (×replication 3 ≈ 11 TB).
- Rollups: 1-min data is 6x fewer points (~20 GB/day, or ~60 GB/day if you keep min/max/sum/count), so a year of 1-min rollups is ~7–20 TB. 1-hour rollups are 360x fewer than raw and cost almost nothing to keep for years.
- Index: 10M series × ~200 B of label metadata ≈ 2 GB of inverted index (label → series IDs), small but it must be in memory.
- Write batch: agents batch a few hundred samples per request, so the gateway sees ~5–10K requests/s.

## 3. Core entities and API

Entities: `Series { seriesId, name, labels{host, region, service...} }`, `Sample { seriesId, ts, value }`, `AlertRule { id, query, threshold, for, severity, routing }`.

```
POST /v1/ingest                 { samples: [{name, labels, ts, value}] }  -> 204
GET  /v1/query_range?query=sum(rate(http_errors{svc="api"}[5m]))&start=&end=&step=60s
POST /v1/alert-rules            { query, condition, for, notify }
```

## 4. High-level design

!Metrics Monitoring - Diagram.excalidraw

- **Collection:** a local agent per host (or a pull-based scraper like Prometheus) batches samples and sends them to the Ingest Gateway.
- **Buffer:** Kafka decouples ingestion from storage, so a TSDB slowdown or restart does not drop data. Topic partitioned by `hash(seriesId)`.
- **Storage:** TSDB writers (consumers) append to a sharded time-series database. Series are placed by consistent hashing so one series always lands on the same shard.
- **Alerting:** the Alert Evaluator consumes the same stream (or queries the TSDB on a schedule), evaluates rules, and sends notifications.
- **Query:** the Query Service fans out to shards, merges partial aggregates and picks the right resolution from rollups.

## 5. Deep dives

### 5.1 Push vs pull collection

| Model | Pros | Cons |
|---|---|---|
| **Pull** (Prometheus) | Central control of targets and rate, easy "is it up?" signal | Needs service discovery, awkward for short-lived jobs and firewalls |
| **Push** (Datadog agent, StatsD) | Works through NAT, short-lived jobs, no service discovery on the server | Servers need back-pressure and per-tenant rate limits |

For a multi-tenant platform use push through an agent, and give the agent local buffering (disk) so network blips do not drop data. Both models can coexist.

### 5.2 TSDB write path and storage

!Metrics Monitoring - Deep Dive Diagram.excalidraw

- Writes append to a **WAL** (durability) and to an in-memory **head block** of compressed chunks, so recent data is queryable immediately.
- Every ~2 h the head is flushed as an immutable block (chunks + label index) on local SSD. A background **compactor** merges small blocks into larger ones and applies retention.
- Old blocks are shipped to **object storage (S3)** for cheap long-term retention (Thanos/Mimir/Cortex pattern).
- **Why a TSDB and not Postgres/Cassandra:** writes are append-only with a very regular shape, so a purpose-built engine gets 10–20x compression and fast range scans. A generic row store pays 16+ B/sample and indexes you do not need. Cassandra can work (wide rows by series + time bucket, TTL) but queries are poor.
- Compression: timestamps as delta-of-delta (mostly 0, 1 bit), values XOR with the previous value (leading/trailing zeros stripped).

### 5.3 Sharding, replication and the index

- Shard by `hash(seriesId)`, replicate each series to 2–3 nodes (quorum write, any-replica read). Query results are merged and de-duplicated across replicas.
- Inverted index `label=value -> posting list of seriesIds` resolves selectors (`{service="api", region="eu"}`) by intersecting lists.
- **High cardinality** (user ID, request ID or URL as a label) explodes the series count and the index. Enforce per-tenant series limits, reject or drop offending labels at the gateway, and alert on cardinality growth.

### 5.4 Querying and rollups

- A background job (or the compactor) computes **rollups**: 1-min and 1-h `min/max/sum/count` per series (keep sum + count, not avg, so averages can be recombined).
- The Query Service chooses the resolution from the requested range and step: ≤ 6 h → raw, ≤ 7 d → 1 min, longer → 1 h. This bounds points per graph to a few thousand.
- Execution: push down filters and partial aggregation to shards (`sum by region`), then merge at the coordinator. Percentiles must use histograms/sketches (t-digest, DDSketch), since percentiles of percentiles are wrong.
- Cache results for popular dashboards (Redis) with step-aligned keys, and only compute the new tail on refresh.

### 5.5 Alerting

- The evaluator runs each rule on a schedule (every 15–60 s), queries the TSDB (preferring the head block), and tracks state per series: `OK -> PENDING -> FIRING`, with a **`for` duration** to suppress flapping.
- Rules are partitioned across evaluator instances by hash of rule ID, with a leader election or lease (etcd) for failover, and the state is persisted so a restart does not re-notify.
- The **Alert Manager** layer de-duplicates, groups alerts (one page for 50 hosts in the same cluster), applies silences/maintenance windows and routes by severity to PagerDuty/Slack/email, with retries.
- **Watchdog:** a "dead man's switch" alert that must always fire. If the external monitor stops receiving it, the monitoring system itself is down.

### 5.6 Failure modes

- **Kafka or ingest overload:** agents buffer locally, the gateway sheds load by priority (alert-related metrics first) and per-tenant quotas.
- **TSDB node loss:** replicas serve reads, and the WAL replays on restart. A new node streams blocks from S3.
- **Monitoring the monitor:** run a second, minimal instance in another region for critical system metrics.
- **Query storm:** limits on series touched and time range per query, a query timeout, and a separate read path from the write path.

## 6. What interviewers look for

- **Junior:** agents, a store, dashboards, threshold alerts, push vs pull.
- **Mid:** queue for ingest, TSDB rationale, retention and rollups, alert evaluation windows.
- **Senior:** compression math, WAL/head/blocks, cardinality control, partial-aggregate pushdown, histogram/percentile handling, alert dedup and HA, monitoring the monitor.

## 7. Common pitfalls

- Using a relational DB or a generic document store for raw samples
- Querying raw 10 s data for a 90-day graph (no rollups)
- Averaging percentiles or storing only averages in rollups
- Ignoring high-cardinality labels
- Alert evaluator as a single instance with no state persistence, or alerts that notify on every evaluation (no `for` or dedup)
