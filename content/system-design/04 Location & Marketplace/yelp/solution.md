---
topic: "Location & Marketplace"
difficulty: Medium
problem: "Yelp"
---
# Design Yelp (Local Business Search and Reviews) – Solution

**Topic:** Location & Marketplace · **Difficulty:** Medium · **Question:** Yelp - Question

## 1. Requirements

**Functional**
- Search businesses by keyword plus location (radius or map bounds), with filters and sorting
- View a business page (details, rating, recent reviews)
- Post a review (rating + text); one review per user per business
- Business rating reflects new reviews

**Non-functional**
- Low-latency search (< 200 ms p95), high availability
- Search is **eventually consistent**: a new review or business edit may take seconds to minutes to appear in results
- Reads vastly outnumber writes
- Review writes must be correct (no duplicates, rating not corrupted)

**Out of scope:** photo upload pipeline, ads, recommendation feeds, owner dashboards, spam ML.

## 2. Back-of-envelope

- 10M businesses × ~2 KB ≈ **20 GB** of business data. Small: one Postgres primary plus replicas handles it.
- 500M reviews × ~1 KB ≈ **500 GB**, growing by maybe 1-2M/day, which is ~20/s. This needs sharding eventually, but write rate is low.
- Search traffic: 100M MAU, say 10M searches/hour at peak ≈ 3K/s. Business page views are ~3x more, but they are cacheable.
- Search index: 10M docs × ~1 KB indexed fields ≈ 10-20 GB, small enough to replicate on every search node.

## 3. Core entities and API

Entities: `Business { id, name, lat, lng, categories[], priceLevel, hours, avgRating, reviewCount }`, `Review { id, businessId, userId, rating, text, createdAt }`, `User`.

```
GET  /search?q=ramen&lat=..&lng=..&radius=5km&sort=rating&cursor=..   -> [ Business ] 
GET  /businesses/{id}                                                  -> Business + first page of reviews
GET  /businesses/{id}/reviews?cursor=..                                -> [ Review ]
POST /businesses/{id}/reviews    { rating, text }                      -> Review
```

Paginate with cursors, not offsets. The user comes from the auth token.

## 4. High-level design

!Yelp - Diagram.excalidraw

- **Search path:** Search Service queries Elasticsearch/OpenSearch, which holds each business with a `geo_point` plus analysed text fields and filters.
- **Business page:** Business Service reads Redis, falling back to Postgres.
- **Review path:** Review Service inserts into the Reviews DB (unique on `(business_id, user_id)`) and emits an event. A Rating Aggregator consumes events and updates `avgRating`/`reviewCount` on the business, and CDC propagates that into the search index.
- Postgres is the source of truth; Elasticsearch is a derived, rebuildable index.

## 5. Deep dives

### 5.1 Proximity search: what indexes locations?

| Approach | How | Pros | Cons |
|---|---|---|---|
| SQL `lat BETWEEN AND lng BETWEEN` | Two B-tree range scans | No extra system | Intersecting two large ranges is slow; no text relevance |
| PostGIS `ST_DWithin` (GiST/R-tree) | True spatial index | Accurate, good for moderate scale | Text relevance weak; scale-out by hand |
| Geohash prefix in KV/SQL | Store geohash(7), query the cell + 8 neighbours | Simple, any store | Border effects, fixed cell size, ranking by hand |
| Quadtree in memory | Cells split when > N businesses | Adapts to density | Custom code, rebuild and distribution are on you |
| **Elasticsearch `geo_point` + text** | BKD tree for geo, inverted index for text | Geo filter, text match, filters, sort in one query | Eventually consistent; extra component |

**Recommended:** Elasticsearch/OpenSearch. Yelp's workload is "text AND location AND filters AND ranking", which a single search engine does natively. A query = `bool { must: match(q), filter: [geo_distance, price, category, open_now] }`, sorted by a function score mixing text relevance, distance decay, rating (Bayesian average) and review count.
- Since business data is static and 20 GB, shard by geography only if needed. Otherwise a few shards × replicas serve thousands of QPS.
- For map-viewport queries use `geo_bounding_box`; for "near me" use `geo_distance`. Dense areas return many hits, so cap results and rank, or cluster on the client.

### 5.2 Keeping the rating up to date

Never `AVG()` over millions of rows on read. Store aggregates on the business: `ratingSum`, `reviewCount`, `avgRating = sum/count`.
- On a new review: `UPDATE businesses SET rating_sum = rating_sum + :r, review_count = review_count + 1`, which is atomic and order-independent. For edits or deletes apply the delta (`new - old`).
- Doing this synchronously in the review transaction is simple and correct at ~20 writes/s. For a very hot business (100K reviews, bursts) move it to an async aggregator consuming Kafka partitioned by `businessId`, so updates to one business are serialised without row-lock contention. A few seconds of lag is fine.
- Use a **Bayesian/weighted rating** for ranking so a 5.0 from 2 reviews does not beat 4.7 from 2,000.
- Unique constraint on `(business_id, user_id)` blocks duplicate reviews even with double-clicks or retries (return 409, or upsert if edits are allowed).

### 5.3 Syncing the DB and the search index

- **Dual writes are fragile** (the DB succeeds, the index call fails). Prefer CDC (Debezium reading the Postgres WAL → Kafka → indexer) or a transactional outbox, so the index is eventually consistent but never silently diverges.
- Indexer writes are idempotent upserts keyed by `businessId`; version them with `updatedAt` to ignore out-of-order events.
- Batch indexing (bulk API, 1-5 s refresh interval) is much cheaper than per-document commits.
- To rebuild or change mappings, build a new index in the background from a DB snapshot and swap an alias. This also gives disaster recovery.

### 5.4 Reads: business page and reviews

- Business pages are read-heavy and nearly static: Redis cache keyed by `businessId`, with invalidation on edits or short TTL (a few minutes), and a CDN for static assets and photos (S3).
- Reviews table: partition/shard by `business_id` so one business's reviews are co-located; index `(business_id, created_at DESC)` for cursor pagination. Cassandra or DynamoDB with `business_id` as partition key fits too. Postgres is fine up to ~1 TB with partitioning.
- Cache the first page of reviews for popular businesses; invalidate on new review.

### 5.5 Scaling and failure modes

- **Search cluster down/slow:** serve degraded results from cache of popular queries (query + geo cell + page), with timeouts and a circuit breaker. Replicas absorb read load.
- **Hot cities:** query cache keyed by normalised `(q, geohash-cell, filters)` has a high hit rate because many users search the same neighbourhood.
- **Abuse:** rate limit reviews, spam/fake review detection async from the event stream, and hold suspicious reviews out of the aggregate.
- **Multi-region:** read replicas and search replicas per region; reviews written to the home region and replicated.

## 6. What interviewers look for

- **Junior:** sensible entities and APIs, a DB schema, naive radius query.
- **Mid:** knows a plain lat/lng index is inadequate; picks geohash/quadtree/search-engine; precomputed rating; caching.
- **Senior:** search engine as a derived index with CDC/outbox, incremental rating with hot-business handling, ranking (Bayesian), cursor pagination, rebuild/alias swap, failure modes.

## 7. Common pitfalls

- Using only B-tree indexes on latitude and longitude and expecting them to scale
- Computing the average rating on every read
- Dual-writing to DB and search index with no repair path
- Treating the search index as the source of truth
- Offset pagination on search results
- Ignoring geohash cell borders when using prefix queries
