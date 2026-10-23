---
topic: "Storage & Caching"
difficulty: Easy
problem: "Bitly"
---
# Design Bitly (URL Shortener) – Solution

**Topic:** Storage & Caching · **Difficulty:** Easy · **Question:** Bitly - Question

## 1. Requirements

**Functional**
- Create a short URL from a long **Original URL** (optional custom alias, optional expiration date)
- Redirect a **Short URL** to the Original URL

**Non-functional**
- Uniqueness: each short code maps to exactly one Original URL
- Low-latency redirects (< 100 ms)
- High availability (99.99%), with availability favoured over strict consistency on the read path
- Scale: ~1B stored URLs, ~100M DAU, read:write ratio ~1000:1 (reads dominate by far)
- Codes should not be trivially guessable in sequence (our extra requirement)

**Out of scope:** user accounts/auth, rich analytics (mention as an extension).

## 2. Back-of-envelope

- Row: code (7 B) + long URL (~200 B) + metadata (~50-100 B) ≈ 300-500 B
- 1B URLs × ~500 B ≈ **~500 GB**. That fits on a single modern database node, so storage is not the scaling problem; replication is there for availability, and sharding is optional headroom.
- Traffic: 100M DAU with ~1 redirect each ≈ 100M reads/day ≈ **~1.2K/s avg, ~10K/s peak**. At 1000:1 that is only ~100K new URLs/day (~1/s). (Stress variant: if you were told 100M writes/day, i.e. ~1.2K/s, the counter-batching and sharding below become necessary.)
- 7 chars of base62 = 62⁷ ≈ 3.5 trillion codes, far more than the 1B (or even 100B) URLs we need.

## 3. Core entities and API

Entities (as the interview framing names them): **Original URL**, **Short URL**, **User**. Stored as one record:
`Url { shortCode (PK), originalUrl, createdAt, expiresAt, creatorId? }`

```
POST /urls          { longUrl, alias?, expiresAt? }  ->  { shortUrl }
GET  /{code}                                         ->  302 Location: longUrl
```

## 4. High-level design

!Bitly - Diagram.excalidraw

- **Start simple:** one server plus a DB is enough for the first version of the design. The write handler validates the URL, creates the code, stores `code → longUrl` and returns the short URL; the redirect handler looks the code up and answers with an HTTP redirect.
- **Evolved design (diagram):** split into a **Write Service** (backed by the counter) and a **Read Service** (backed by the cache and DB). Both are stateless and scale horizontally behind the gateway; with a 1000:1 ratio the read side must scale on its own.
- **Write path:** the Write Service gets a unique id/code, stores `code → longUrl` and returns the short URL.
- **Read path:** the Read Service checks Redis first, falls back to the DB on a miss, then returns the redirect.

## 5. Deep dives

### 5.1 Generating unique short codes

| Approach | How | Verdict |
|---|---|---|
| Bad: prefix of the URL / raw random number | Take the first chars of the URL, or a random number with no check | Different URLs collide constantly; random numbers give no uniqueness guarantee |
| Good: hash long URL (MD5/SHA → base62, take 7 chars) or random code + uniqueness check | `base62(hash(url))[:7]`; or random 7 chars, insert with unique constraint, retry on conflict | Stateless and simple; same URL → same code for hashing. But truncation causes collisions and the collision rate grows as the table fills (birthday paradox), so you need check-and-retry |
| **Great: unique counter + base62** | Global counter (Redis `INCR`) → base62 encode | No collisions by construction, shortest codes. Costs: sequential codes are guessable, and the counter is a shared dependency |

**Recommended:** a counter in Redis, with fixes. (1) **Counter batching:** each Write Service instance reserves a **batch** of ids (e.g. 1,000) from Redis, so it hits the counter once per batch (and survives short counter outages). (2) Run the id through a reversible scramble (e.g. a Feistel or XOR/permutation) before base62 so codes aren't enumerable. (3) Make the counter durable and highly available: Redis with AOF persistence plus a replica and failover, or one counter per region/shard. If it loses a few ids, nothing breaks, since ids only need to be unique, not dense. Custom aliases bypass the counter and rely on the unique constraint.

### 5.2 Making redirects fast

Baseline: the Read Service looks up `shortCode` in the DB.

1. **Index on the short code.** Make `shortCode` the primary key (a B-tree index) so a lookup is O(log n) rather than a table scan. (A DB with an indexed primary key is already the "good" baseline.)
2. **In-memory cache.** Reads are ~1000:1 vs writes and mappings are **immutable**, so they are ideal for caching. Redis in front of the DB with an LRU policy; the hot set of popular links fits in memory. Caveats: cache invalidation on expiry/delete, and stampedes on a freshly viral link (see 5.5).
3. **CDN / edge.** Push the hottest redirects out to edge compute or a CDN so the request never reaches our region. Trade-offs: invalidation is harder, expiry must be honoured at the edge, and every edge hit hides the click from us (analytics).

- **301 vs 302:** 301 (permanent) lets browsers cache the redirect, which means fewer hits on us but we lose click analytics and can't change or expire the target. 302 (temporary) keeps every click flowing through us. Use **302** if you need analytics or expiry.

### 5.3 Storage choice

Access pattern is pure key-value (`code → record`), with no joins. At ~500 GB, a single Postgres (with replicas) or DynamoDB works fine; neither choice is the point of the question. If the write rate grows, DynamoDB/Cassandra (horizontal by default) or Postgres sharded by `code` with consistent hashing keeps it simple.

### 5.4 Custom aliases and expiry

- Alias: insert with a unique constraint on `code`; return 409 if it exists.
- Expiry: store `expiresAt`; check on read. Clean up in a background job (or a DB TTL feature). Expired entries should also be evicted from the cache.

### 5.5 Scaling and failure modes

- **Scaling the services:** separate read and write services so each scales on its own (reads are ~1000x writes); both are stateless. Scale the DB for availability with replication (and a failover replica); scale the cache with more nodes partitioned by code.
- **Cache stampede** on a viral link: use request coalescing, or a short-TTL local in-process cache in front of Redis.
- **Cache down:** reads fall back to the DB. Protect the DB with rate limiting or circuit breaking.
- **Abuse:** rate limit link creation per IP/user, scan submitted URLs for malware/phishing.
- **Multi-region and failover (Staff+ territory):** replicate the DB across regions. A redirect can be served from the nearest region, and writes can go to any region as long as code ranges (or counters) are partitioned per region. Health-checked failover for the counter, cache and DB; the redirect path should survive the loss of a region.
- **Security and operations:** unguessable codes, HTTPS, rate limits, blocklist/malware scanning, and dashboards/alerts on redirect latency, cache hit ratio and counter headroom.

## 6. What interviewers look for

- **Mid-level:** clear entities and API, a working high-level design, a sound code-generation scheme with collision handling, and an index/cache for fast reads.
- **Senior:** compares code-generation strategies and lands on a counter with batching, explains the read path (index, cache, CDN), 301 vs 302, separate read/write scaling, hot keys, abuse.
- **Staff+:** drives the depth unprompted: multi-region design, failover of the counter/cache/DB, security (guessability, malicious URLs), operational concerns (monitoring, capacity), and where not to over-build.

## 7. Common pitfalls

- Hashing the URL and ignoring collisions (or using a URL prefix as the code)
- A single global counter hit on every write
- Forgetting that 301 kills analytics
- Over-engineering (Kafka, microservice sprawl) for what is a simple KV problem
