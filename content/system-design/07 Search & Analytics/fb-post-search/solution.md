---
topic: "Search & Analytics"
difficulty: Hard
problem: "FB Post Search"
---
# Design Facebook Post Search – Solution

**Topic:** Search & Analytics · **Difficulty:** Hard · **Question:** FB Post Search - Question

## 1. Requirements

**Functional**
- Users create posts and like posts
- Keyword search over posts, returning a paginated list, **sorted by recency or by like count** (a `sort` parameter)
- Extensions (mention, do not build first): edit/delete, relevance ranking blended with recency/popularity, privacy-aware visibility filtering

**Non-functional**
- Median search latency < 500 ms (we also track p99), with high request volume
- New posts searchable within **< 1 minute** (near-real-time)
- All posts discoverable, including old ones, but older content may be slower
- High availability for search, while eventual consistency with the post store is fine
- Efficient storage: the index is large, so cost matters

**Out of scope:** fuzzy matching/typos, personalisation, sophisticated ranking, media (image/video) search, real-time result updates, typeahead, ads. Privacy filtering is treated as an extension (5.6), assuming public posts by default.

## 2. Back-of-envelope

- 1B users × ~1 post/day ≈ 1B posts/day ≈ **~10K posts/s** of index writes. With ~10 likes per user per day: **~100K likes/s**. Searches: **~10K QPS**. The system is **write-heavy** (likes dominate), unlike most search systems.
- Storage: ~1 KB per post × 1B/day × 365 × 10 years ≈ 3.6T posts ≈ **~3.6 PB** of raw posts (kept in the post store). The search index stores IDs plus ranking features, ~300-500 B per post, so ~1-2 PB of index, which must be sharded. A single Lucene shard is kept to ~30-50 GB, so **tens of thousands of shards** in total.
- Recent content (last ~7 days, ~7B posts) is ~3 TB of index, which fits on a modest cluster in RAM + SSD and serves most queries.
- Likes: updating the index on every like would be 100K writes/s on top of 10K posts/s, so see 5.5.

## 3. Core entities and API

Entities: `User`, `Post { postId, authorId, text, createdAt, visibility, likeCount }`, `Like { postId, userId }` (tracked mainly as a **count**, not as individual events in the index), and the derived `IndexDoc { postId, terms, createdAt, likeBucket }`.

```
POST /posts                { text }                                       -> { postId }
POST /posts/{postId}/like                                                 -> 200
GET  /search?q=pasta+recipe&sort=recent|likes&cursor=...&limit=20         -> { posts[], nextCursor }
```

## 4. High-level design

!FB Post Search - Diagram.excalidraw

- **Write path (posts):** Post Service writes the post to the source-of-truth store, then publishes `PostCreated/Updated/Deleted` to **Kafka**. Indexers consume, tokenise and update the **inverted index** (keyword -> post IDs). This keeps the post write latency independent of indexing and lets the index be rebuilt by replaying Kafka/the post DB.
- **Write path (likes):** Like Service increments the per-post like count and forwards only **milestone** updates (1, 2, 4, 8, ... likes) to the index via Kafka (5.5).
- **Read path:** requests pass a **CDN / search cache** (short TTL), then the API Gateway (auth, rate limiting) and the Search Service. Search scatters the keyword query to the index shards, merges the top results, re-ranks the top candidates with fresh like counts from the Like Service, and hydrates post bodies from the post store/cache. Optional: ACL/visibility check against the social graph (5.6).

## 5. Deep dives

### 5.1 Why an inverted index

Mapping `term -> sorted list of postIds (posting list)` turns a keyword query into list intersection (AND) or union (OR) over sorted integers, in time proportional to the lists, not the corpus. A `LIKE '%pasta%'` is a full scan. Postings are compressed (delta + variable-byte / PForDelta), skip pointers speed up intersections, and per-term statistics (doc frequency) feed BM25 scoring.

| Option | Verdict |
|---|---|
| SQL `LIKE`/full-text index in Postgres | Fine up to millions of rows, cannot sustain trillions of docs and 10K QPS |
| **Lucene-based engine (Elasticsearch/OpenSearch/Solr)** | Strong default: segments, BM25, near-real-time refresh |
| Custom index (as large companies do) | Justified only at extreme scale, mention but do not build |

### 5.2 Sharding the index

- **Shard by document** (postId or time range): every shard holds a full index of its subset of posts. A query is sent to all shards, each returns its local top-K, and a broker merges them. Simple to update (a post touches one shard) and balances load well.
- **Shard by term**: a query hits only the shards that own its terms, but multi-term queries need to ship large posting lists across the network, and hot terms ("the", "covid") create hotspots. Rejected.
- Choose **document sharding, partitioned by time** (then hash within a time bucket). Time partitioning means a "last 24h" query touches few shards, and old shards are immutable and cheap to replicate and compress.
- **Scatter-gather** latency is driven by the slowest shard, so use replicas, send hedged requests after p95, and return partial results if a shard times out.

### 5.3 Freshness and the write path

- Each shard buffers new docs in memory and exposes them on a refresh (~1 s in Lucene), flushing to immutable segments that are merged in the background.
- Updates (likes) should not reindex the document on every like. Keep volatile counters in a **separate engagement store** (the Like Service) and fetch them at ranking time; the index only sees milestone updates (5.5). Deletes are tombstones applied at query time and cleaned up on merge.
- Kafka is partitioned by postId to keep per-post ordering of create → edit → delete. Indexers are idempotent (upsert by postId + version).
- If the indexer lags, the pipeline back-pressures through Kafka without hurting the post write path.

### 5.4 Tiered index (cost and latency)

!FB Post Search - Deep Dive Diagram.excalidraw

Most searches target recent posts. Tiers: **real-time** (last ~1 day, memory-heavy, many replicas), **warm** (weeks/months, SSD), **archive** (older, HDD, few replicas, higher latency allowed). The broker queries tiers in order of recency and can stop early once it has enough good results, or only touch the archive when the user asks for older content. This is the main cost-saver.

### 5.5 Sort modes, high like volume and ranking

- **Sort by recency:** postings sorted by `createdAt` (new posts are appended), so the top page is a cheap read of the head of each list.
- **Sort by likes:** postings must be ordered by like count, but 100K likes/s cannot all hit the index.
  - *Good:* batch likes over a window (~30 s) before writing to the index. Little help for non-viral posts, which get a like here and there.
  - *Great (recommended): milestone updates + two-stage retrieval.* Write a post's new like count to the index only when it crosses a power of two (1, 2, 4, 8, ...), so 1,000 likes cost ~10 index writes. The index is therefore an approximate ordering. Retrieve the top **2N** candidates per keyword from it, fetch their exact, fresh counts from the Like Service (a cache/counter store), re-sort and return the top N.
- **Optional relevance ranking (extension):** L1 per shard returns the top ~200 by BM25 + static score (recency decay, engagement); an L2 model (GBDT/small NN) re-scores the merged ~500 with searcher-author affinity and history.
- Pagination uses a **cursor** (sort value + postId), not an offset, so deep pages stay cheap and stable.

### 5.6 Privacy and visibility (extension)

- The classic mistake is filtering after ranking and showing empty pages. Do both: **pre-filter** coarsely, **post-filter** exactly.
- Index a `visibility` field (public / friends / custom list) and the `authorId`. For public posts, no per-user check is needed. For friends-only posts, add the searcher's friend set (or a bounded set of friends the searcher interacts with) as a filter on `authorId`, fetched from the social graph service (cached).
- The final authority is the post store ACL check on the top ~100 results before hydration, so a stale index can never leak data. Over-fetch (e.g. 3x) to compensate for filtered-out results.
- Deleted/blocked content is removed via the tombstone path, and the final ACL check guards the lag window.

### 5.7 High request volume (caching)

- *Good:* a distributed cache (Redis) next to the Search Service keyed by `(query, sort, page)` with a TTL under a minute, matching the freshness requirement. Add request coalescing for viral queries.
- *Great (recommended):* **CDN edge caching** with `Cache-Control` headers (short max-age), so popular queries are answered near the user in tens of ms instead of hundreds. The same short TTL keeps results within the < 1 minute freshness budget.

### 5.8 Multi-keyword and phrase queries

- *Good:* **intersect and filter.** Fetch the posting list per term, intersect the sorted ID sets, then check the post text for the exact phrase. Cost grows with big lists (megabytes of IDs for common words) and the phrase check happens at request time.
- *Great (recommended):* **bigram/shingle indexing.** Also index adjacent word pairs ("taylor swift" as one key), so a phrase becomes a single lookup. Trade-off: the key space explodes (e.g. ~10M single-word keys to 100M+ with bigrams), so only index bigrams that are frequent enough, and fall back to intersect-and-filter for the rest. (Lucene-style positional postings are the alternative.)

### 5.9 Storage optimisation

- **Cap the posting list per keyword** (~1K-10K entries for each sort order). Only the top entries are ever served, since users rarely page deep.
- **Tier by temperature:** hot keywords in Redis/memory, cold keywords in blob storage (S3). **Lazy-load**: query the hot tier first and fall back to the cold tier only on a miss. This pairs with the time-based tiers in 5.4.

### 5.10 Failure modes and hot spots

- **Shard replica down:** other replicas answer, and a failed shard is rebuilt from Kafka replay + the last snapshot in object storage.
- **Viral topic / hot query:** cache query -> result IDs for a few seconds (Redis), with request coalescing.
- **Reindexing** (schema change): build a new index alias in the background, dual-write, swap atomically.
- **Spam / abuse:** filter in the ingest pipeline, not at query time.

## 6. What interviewers look for

- **Mid-level:** clear APIs and data model; both the ingestion path (post/like -> index) and the query path; inverted index idea; a queue to feed the index. Mostly breadth, and the interviewer may drive the later stages.
- **Senior:** anticipates the problems unprompted (write volume of likes, storage size, request volume) and articulates trade-offs; document sharding with scatter-gather, near-real-time indexing, caching (distributed cache vs CDN), phrase queries, tail latency and hedging.
- **Staff+:** deep, "been there" detail: milestone like updates with re-ranking from fresh counts, bigram index trade-offs, keyword caps and hot/cold tiering, separate engagement store, reindexing strategy, cost estimates, privacy filtering without leaks; spots issues before they surface and brings the interviewer new insight.

## 7. Common pitfalls

- Using the primary database for text search or writing synchronously to the index in the post request
- Sharding by term without considering hot terms and multi-term joins
- Re-indexing a document every time it gets a like (100K likes/s will melt the index), instead of milestone updates plus fresh counts at read time
- Applying privacy filters only in the UI or only after pagination
- Ignoring cost: keeping 10 years of posts on the same hardware as yesterday's posts
