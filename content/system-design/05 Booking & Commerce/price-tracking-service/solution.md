---
topic: "Booking & Commerce"
difficulty: Medium
problem: "Price Tracking Service"
---
# Design a Price Tracking Service – Solution

**Topic:** Booking & Commerce · **Difficulty:** Medium · **Question:** Price Tracking Service - Question

## 1. Requirements

**Functional**
- Add a product to track via URL (web or browser extension)
- View price history for a product
- Create alerts (price below X, percent drop, back in stock); get notified by email/push
- Keep prices fresh by regularly fetching them from retailers

**Non-functional**
- Eventual freshness: hot products within ~15 min, long tail within ~24 h
- Notification delay < a few minutes after the price change is observed
- Read-heavy chart/history API with low latency; highly available
- Be a polite crawler: respect robots.txt, rate limits, terms of service; prefer official/affiliate APIs

**Out of scope:** price prediction/ML, product search across retailers, payments for premium plans.

## 2. Back-of-envelope

- 50M products. If 5M "hot" products refresh every 15 min and 45M refresh daily: 5M/900 s ≈ 5.5K/s + 45M/86,400 ≈ 520/s ≈ **~6K fetches/s**. At ~200 ms and 50 KB per page that is ~300 MB/s of inbound bandwidth: a fleet of a few hundred fetchers.
- **Most fetches return an unchanged price** (>90%), so store only **changes** (plus a last-checked time): ~5% of 6K/s ≈ 300 new points/s ≈ 26M/day ≈ 10B/year × ~40 B ≈ **~400 GB/year**. Cheap.
- Alerts: 100M rows × ~100 B = 10 GB. Fits in a single big Postgres instance (sharding is optional).
- Chart reads: say 20M page views/day ≈ 230/s. Trivial with a cache.

## 3. Core entities and API

Entities: `Product { id, retailer, canonicalUrl, title, currentPrice, lastCheckedAt, nextCheckAt, watchers }`, `PricePoint { productId, ts, price, currency, inStock }`, `Alert { id, userId, productId, type, threshold, status, lastNotifiedAt }`, `User`.

```
POST /watches            { url }                          -> { productId }
GET  /products/{id}/history?range=1y                      -> [{ts, price}]
POST /alerts             { productId, type, threshold }   -> { alertId }
DELETE /alerts/{id}
```

## 4. High-level design

!Price Tracking Service - Diagram.excalidraw

- **User-facing:** Tracker API on Postgres (users, products, alerts) and a time-series store for price history.
- **Crawl pipeline:** the **Scheduler** picks products whose `nextCheckAt` is due and emits fetch jobs; **Fetchers** (with a proxy pool) get the price from retailer pages or APIs and publish an observation to **Kafka**.
- **Processor:** consumes observations, normalizes and validates the price, appends a point only if changed, updates `currentPrice`, and evaluates alerts. **Notification Service** sends emails/push with idempotency.

## 5. Deep dives

### 5.1 Crawl scheduling and priorities

- `nextCheckAt` is derived from a **priority score**: number of watchers, recent volatility (items that changed lately are checked more often), alert proximity (price within 10% of someone's threshold), and the retailer's budget. Popular items every 15 min, stale ones back off exponentially to a max of 1 week.
- Implementation: a priority queue in Redis (ZSET keyed by `nextCheckAt`) or a Postgres index on `nextCheckAt` polled in batches; sharded by `hash(productId)` across scheduler instances.
- **Per-domain politeness:** a token bucket per retailer (e.g. 5 req/s per IP pool) and jittered scheduling so requests are spread out, not bursty. Dedupe: one fetch per canonical product even if 100K users watch it.
- Event-driven boost: when a user adds a new product, fetch immediately and get a first price in seconds.

### 5.2 Fetching reliably

| Source | Pros | Cons |
|---|---|---|
| Official/affiliate API | Stable, legal, structured | Quotas; limited retailers |
| HTML scraping with per-site parsers | Works everywhere | Fragile; blocks and CAPTCHAs; legal/ToS risk |
| Crowd-sourced prices from browser extension | Free, real regional prices | Trust, spam, needs validation |

- Fetchers run in a pool with rotating egress IPs; retries with backoff on 429/5xx, dead-letter queue for repeated failures.
- **Parser versioning and validation:** reject outliers (price drop > 90% or 0) or require a second confirmation fetch before alerting; alert on parser failure rate per site, so layout changes are noticed in minutes.
- Normalize canonical URLs and product identifiers (ASIN/EAN/GTIN) so that `?tag=` variants are the same product.

### 5.3 Storing price history

- Append-only time series keyed by `(productId, ts)`. Options: **TimescaleDB** (Postgres extension, compression, continuous aggregates) or **Cassandra/DynamoDB** with partition key `productId` and clustering key `ts`. Rejected: one big Postgres table with a plain index, which is workable at first but needs partitioning by time/hash later.
- Store **change points only**; the chart fills the gaps with "price stays until next point". Rollup old data (daily min/max after 1 year).
- Cache the chart JSON for hot products in Redis/CDN (TTL ~5 min, invalidate on a price change).

### 5.4 Matching prices to alerts

- 100M alerts: never scan. Index alerts by `productId`; on each *changed* price (300/s), fetch alerts for that product ordered by threshold: `WHERE productId=? AND status='ACTIVE' AND threshold >= newPrice`. A composite index `(productId, threshold)` makes this a range scan.
- A product with 500K watchers produces a large fan-out: process in batches and enqueue notification jobs rather than sending inline.
- Percent-drop and all-time-low alerts: precompute `minPrice`/`price7dAgo` on the product row so the matcher stays O(1) per alert.
- **No-flap rule:** mark `lastNotifiedAt` and the price at notification; re-arm only if the price goes back above the threshold or after a cooldown.

### 5.5 Notifications

- Kafka topic `notifications`, keyed by `userId`; sender workers are idempotent via a dedup key `alertId:pricePointId`. Email via SES/SendGrid-like providers, push via FCM/APNs; user-level rate limiting and digest mode.
- Verify the price once more just before sending if the observation is older than a few minutes.

### 5.6 Scale and failure modes

- Fetchers and processors are stateless; autoscale on Kafka lag. If processing falls behind, prioritize products with active alerts.
- A retailer blocks us: circuit-break that domain, fall back to API/crowd data, and slow its schedule instead of hammering.
- Multi-region is not needed for correctness; replicate Postgres for read availability.

## 6. What interviewers look for

- **Junior:** user flow, API, a cron-based fetcher, store price history.
- **Mid:** scheduler with priorities, Kafka between fetch and processing, time-series storage, alert indexing by product.
- **Senior:** crawl budget economics (dedupe, adaptive frequency, politeness), change-only storage, parser validation/outlier handling, fan-out for popular products, idempotent notifications and flap control, legal/ToS considerations.

## 7. Common pitfalls

- Fetching every product at the same frequency
- Re-fetching the same product once per watcher
- Scanning all alerts on each price update
- Storing a row per check instead of per change
- Trusting scraped prices blindly (a parse bug sends 100K false "90% off" emails)
- Ignoring blocking, rate limits and legal constraints of crawling
