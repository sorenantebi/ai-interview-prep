---
topic: "Social & Feeds"
difficulty: Medium
problem: "News Aggregator"
---
# Design a News Aggregator – Solution

**Topic:** Social & Feeds · **Difficulty:** Medium · **Question:** News Aggregator - Question

## 1. Requirements

**Functional**
- Ingest articles continuously from many publishers (RSS/Atom, sitemaps, HTML)
- Group articles about the same event into a story cluster
- Serve a feed by topic and region (top stories, latest), with title, snippet, thumbnail and link-out
- Keyword search over recent articles

**Non-functional**
- Freshness: breaking news visible within 1 to 2 minutes
- Read latency < 200 ms, high availability on the read side
- Politeness: respect robots.txt and per-site rate limits
- Scale: 100K sources, 10M fetched articles/day, 50M DAU

**Out of scope:** user accounts and heavy personalization, paywalls, ad system, full-text republishing (copyright). We store snippets and link out.

## 2. Back-of-envelope

- Article ingest: 10M/day ≈ **115/s average**, 5x on busy hours. Modest.
- Source polling: 100K sources, with hot sources every 1 to 5 minutes and the long tail every hour → roughly **~300 to 500 feed fetches/s**.
- Storage: extracted text + metadata ~10 KB per article → **100 GB/day, ~36 TB/year**. Raw HTML (~100 KB) is kept short-term (say 7 days) in S3, ~1 TB/day.
- Reads: 50M × 10 = 500M/day ≈ **6K/s average, ~20K/s peak**. Top-story pages are the same for everyone in a region and topic, so a cache hit rate above 95% is realistic.
- Search index: only recent window (e.g. 30 days, ~100M docs) is hot.

## 3. Core entities and API

Entities: `Source { sourceId, feedUrl, region, crawlInterval, authority }`, `Article { articleId, sourceId, url, canonicalUrl, title, snippet, publishedAt, contentHash, storyId, topics[] }`, `Story { storyId, articleIds[], headline, score, updatedAt }`.

```
GET /feed?topic=tech&region=de&cursor=&limit=20   -> { stories[], nextCursor }
GET /stories/{storyId}                            -> { articles[], timeline }
GET /search?q=...&cursor=                         -> { articles[] }
```

Each story in the feed carries the lead article, a few alternate sources, and a thumbnail URL served via CDN.

## 4. High-level design

!News Aggregator - Diagram.excalidraw

- **Ingestion (write path):** a scheduler decides which sources to crawl, crawler workers fetch feeds and pages, raw results go to Kafka, processing workers extract text, dedupe, cluster and classify, then write to the article store and the search index.
- **Ranking:** a ranker combines story signals (number of sources, source authority, freshness, click-through) and writes ordered top-story lists per topic/region into Redis.
- **Serving (read path):** Feed Service reads precomputed lists from Redis, hydrates story and article metadata, and falls back to Elasticsearch on misses or long-tail topics. The CDN caches popular feed pages for short TTLs (10 to 30 s).

## 5. Deep dives

### 5.1 Crawling and freshness

| Technique | Pros | Cons |
|---|---|---|
| Fixed-interval polling of RSS | Simple | Wasteful for quiet sources, slow for busy ones |
| **Adaptive polling** | Interval per source learned from its historical posting rate (EWMA), clamped to e.g. 1 min to 6 h; uses `ETag` / `If-Modified-Since` | Needs a scheduler and state |
| WebSub (PubSubHubbub) / publisher pings, sitemap news feeds | Near-instant, cheap | Only for cooperating publishers |
| Full-page scraping | Works without feeds | Fragile, per-site parsers, legal/ToS risk |

Use push where offered, adaptive polling otherwise. The scheduler is a priority queue keyed by `nextFetchAt`, sharded by source hash. Crawlers enforce per-domain concurrency and delay (robots.txt `Crawl-delay`), back off on 429/5xx, and use a circuit breaker per domain. Fetches are idempotent, results carry a `fetchId`.

### 5.2 Deduplication and story clustering

Three layers, cheapest first:
1. **Exact duplicates:** normalize the URL (strip tracking params like `utm_*`, follow canonical tags, lowercase host), hash it, check a Redis set / Bloom filter. Drop republished or re-fetched articles.
2. **Near-duplicates (syndicated wire copy):** SimHash or MinHash over the text shingles with an LSH index, so a Hamming distance below ~3 bits on a 64-bit SimHash means "same text".
3. **Same event, different wording:** embed title + lead paragraph with a sentence-embedding model and find nearest stories in a recent-window ANN index (e.g. FAISS/HNSW, or Elasticsearch kNN) with a similarity threshold plus entity and time checks. Join the best story or create a new one.

!News Aggregator - Deep Dive Diagram.excalidraw

Clustering is eventually consistent. Clusters can merge later (two stories turn out to be the same), so store `storyId` aliases with a merge pointer instead of rewriting all articles synchronously.

### 5.3 Ranking and topic classification

- Classification (topic, region, language, entities) runs in the processing worker; a small text classifier is enough.
- Story score ≈ freshness decay × number of independent sources × average source authority × engagement (click-through, dwell) + category boosts. Stream signals update scores within seconds; heavier batch features refresh hourly.
- The ranker materializes lists `top:{topic}:{region}` in Redis sorted sets. Anonymous reads are cache-friendly. Light personalization can re-order a precomputed candidate set per user at read time rather than precomputing per user.

### 5.4 Storage choices

| Data | Store | Why |
|---|---|---|
| Raw HTML | S3, lifecycle delete after days | Large, rarely read |
| Article + story metadata | Cassandra / DynamoDB (or sharded Postgres) | Write heavy, key lookups by id and by (topic, time) |
| Search and recent-story queries | Elasticsearch / OpenSearch, time-based indices | Full text, filters, aggregations |
| Ranked lists | Redis sorted sets | Latency |
| Source config and scheduler state | Postgres | Small and relational |

### 5.5 Serving at scale

- Cache the whole response per `(topic, region, page)` in the CDN for seconds, and in Redis for the ranked ids. A breaking story causes a spike on the same keys: short TTL plus request coalescing prevents stampedes.
- Cursor pagination on `(score, storyId)`, which stays stable even as scores change (snapshot id in the cursor).
- Thumbnails are fetched once, resized and stored on S3/CDN (do not hotlink publisher images).

### 5.6 Failure modes

- **Slow or broken publishers:** per-domain timeouts, retries with exponential backoff and jitter, quarantine after repeated failures.
- **Duplicate processing:** Kafka at-least-once; processing is idempotent via `contentHash` and article-id upsert.
- **Backlog on a big event:** scale processing workers on consumer lag; prioritize recent articles and high-authority sources with separate priority topics.
- **Spam and low-quality sites:** source authority score, blocklists, demote content farms.
- **Index outage:** Redis lists still serve the main feed, search degrades.

## 6. What interviewers look for

- **Junior:** crawler to database to feed API; polling RSS; simple ranking by time.
- **Mid:** queue-based pipeline, separate read and write paths, caching, search index, dedupe by hash.
- **Senior:** adaptive scheduling and politeness, layered near-duplicate detection and clustering, ranking signals, precomputed lists, freshness vs. cost trade-offs, backpressure and failure isolation.

## 7. Common pitfalls

- Treating it as a plain CRUD app and ignoring ingestion scale and politeness
- Hammering publishers or ignoring robots.txt
- Only exact-hash dedupe, so syndicated and rephrased stories flood the feed
- Ranking on read over the whole corpus instead of precomputing lists
- Storing and republishing full copyrighted text
- One giant synchronous pipeline with no queue or retry story
