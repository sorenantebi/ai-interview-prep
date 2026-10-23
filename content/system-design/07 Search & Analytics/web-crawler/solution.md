---
topic: "Search & Analytics"
difficulty: Medium
problem: "Web Crawler"
---
# Design a Web Crawler – Solution

**Topic:** Search & Analytics · **Difficulty:** Medium · **Question:** Web Crawler - Question

## 1. Requirements

**Functional**
- Starting from seed URLs, crawl the web: fetch pages, extract outgoing links, and add unseen links to the crawl
- Extract and store the text data for downstream consumers (LLM training, indexing); raw HTML is kept in blob storage

**Non-functional**
- Scale: ~10B pages (~2 MB average) crawled in ~5 days
- Fault tolerant: a crashed worker must not lose progress or redo large amounts of work
- Polite: honour `robots.txt` and a per-host request rate
- Efficient: no repeated fetches of the same URL or the same content
- Extensible: allow new content types (images, PDFs) by plugging in new processors

**Out of scope:** JavaScript rendering (mention as an extension), non-text media, authenticated pages, text post-processing, search/ranking, and the downstream training pipeline.

## 2. Back-of-envelope

- 10B pages / (5 days × 86,400 s) ≈ **~23K pages/s**
- Page size ~2 MB average → ~46 GB/s ≈ **~370 Gbps** sustained download. Network, not CPU, is the bottleneck.
- A network-optimized instance with ~200 Gbps NICs realistically sustains ~30% utilisation (~60 Gbps ≈ 7.5 GB/s) ≈ **~3,750 pages/s**. So **~8 such machines** finish in ~4 days (10B / 3,750 / 8 ≈ 3.9 days). The alternative is a larger fleet of small machines. Check concurrency too: 23K pages/s × ~1 s latency means ~23K connections in flight, which async I/O handles.
- Raw storage: 10B × 2 MB = ~20 PB of HTML in object storage (S3), a few PB after gzip. Only the extracted text (a small fraction) is the real product.
- URL-seen set: 10B × 8-byte fingerprint = **80 GB**, which is small enough to shard across a few Redis/memory nodes. A Bloom filter at 1% false positives needs ~10 bits/URL ≈ 12 GB.
- Each page has ~50 links, so ~500B extracted URLs. Most are duplicates, which is why the dedup stage must be cheap.

## 3. Core entities and API

Entities: `UrlTask { url, host, depth, priority, attempts, nextEligibleAt }` (frontier message), `Page` / URL metadata row `{ urlHash, domain, contentHash, s3Key, textKey, fetchedAt, status, depth }` (in the **Metadata DB**, e.g. DynamoDB or Postgres), `HostState { host, robotsRules, crawlDelay, nextAllowedAt }` (Redis).

The crawler is a pipeline, so the "API" is internal queue messages, not a public REST API:
```
frontier.pop(workerId)            -> [UrlTask]           (lease with visibility timeout)
frontier.push(urls[])             -> void
pageStore.put(urlHash, html)      -> s3Key
```

## 4. High-level design

!Web Crawler - Diagram.excalidraw

Crawl loop:
1. Seed URLs are pushed into the **URL Frontier** (a queue with leases, retries and a DLQ).
2. A **Fetcher** pulls a URL, resolves the host via a caching **DNS resolver**, checks cached `robots.txt` and the **per-domain rate-limit store** (Redis), and downloads the page.
3. The raw HTML is written to **blob storage** (S3) and a metadata row is recorded in the **Metadata DB**.
4. The **text / URL extraction** stage (parser) reads the HTML, stores the extracted text, computes a content hash, and extracts links.
5. New links are normalised and checked against the Metadata DB / URL-seen set. Content whose hash is already known is not processed again. Surviving URLs go back into the frontier.
6. Fetch and parse stages are stateless and scale independently (parsers by queue depth), so a dead machine only means its leased URLs reappear.

## 5. Deep dives

### 5.1 The frontier: priority plus politeness

Implement the frontier as a set of queues, not one global queue.

!Web Crawler - Deep Dive Diagram.excalidraw

- **Front queues** (priority): a prioritizer scores each URL (domain authority, depth, change frequency) and puts it in one of N queues.
- **Back queues** (politeness): each host maps to exactly one back queue (`hash(host)`), and every fetcher worker owns a set of back queues. A min-heap keyed by `nextAllowedAt` tells it which host may be hit next.
- After each fetch, `nextAllowedAt = now + max(crawlDelay, 10 × lastFetchLatency)`. This stops 1,000 machines hammering the same site.
- **Per-domain rate limit:** keep a Redis counter per domain (sliding window, about 1 request/s, or the `Crawl-delay` from `robots.txt` if larger) and add random **jitter** to retries so blocked workers do not wake up in lock-step. `robots.txt` is parsed once per host, cached, and `Disallow` rules are honoured before queueing.
- Physical implementation: Kafka partitions or SQS per shard would give durability, but per-host delay is awkward there. Common approach: a sharded Redis/RocksDB-backed frontier with `ZSET(score = nextAllowedAt)` per shard, or Kafka partitioned by host plus an in-memory scheduler per consumer.

### 5.2 Fault tolerance and retries

Where do the retry timers live? In-process timers (**bad**) vanish with the worker. Hand-built retry topics on Kafka (**good**) work but you write the delay and DLQ logic yourself. A queue with a **visibility timeout** and a way to change it per message (SQS `ChangeMessageVisibility`, giving exponential backoff plus a built-in DLQ) is the **great** choice, because the lease, retry and dead-letter behaviour come with the queue.

| Failure | Handling |
|---|---|
| Fetcher dies mid-page | URL was **leased** with a visibility timeout (SQS-style or a lease column). Timeout expires, the URL goes back in the queue. Fetching twice is harmless because storage is idempotent on `urlHash`. |
| Transient error (503, timeout) | Retry with **exponential backoff**: 1 min, 10 min, 1 h, then give up. Store `attempts` on the task. |
| Permanent error (404, 410, DNS NXDOMAIN) | Mark the URL dead, do not retry. |
| Poison URL (parser crashes) | After N attempts, move to a **dead-letter queue** for inspection. |
| Frontier shard lost | Frontier state is persisted (Kafka log / replicated Redis with AOF). A periodic snapshot is the recovery point. |

Do not use "one big transaction": pipelining stages (fetch → store → parse → enqueue) with at-least-once delivery between stages and idempotent writes is simpler and faster.

### 5.3 Deduplication

| Level | Technique | Notes |
|---|---|---|
| URL | Normalise (lowercase host, strip fragment, sort query params, drop tracking params, resolve `..`), then check a fingerprint set | Redis `SET`/hash sharded by URL fingerprint (80 GB), or a Bloom filter (12 GB, accepts rare false positives = a page skipped, fine for crawling) |
| Content | Hash of the page body (SHA-256) catches exact copies; **simhash/minhash** catches near-duplicates (mirrors, boilerplate changes) | Hash stored (indexed) in the Metadata DB or a Bloom filter; skip link extraction if content already seen. A false positive only means one page is skipped |

A rejected approach is a SQL `SELECT 1 FROM urls WHERE url = ?` per link: 500B lookups cannot go through a relational index.

### 5.4 DNS, robots.txt and connection efficiency

- DNS is a hidden bottleneck at 23K req/s. Run a local caching resolver per fetcher fleet, cache by host with TTL, and keep results warm because the frontier already groups URLs per host. Spread lookups over several DNS providers (round-robin) so none of them rate-limits you.
- Fetch `robots.txt` once per host, cache it (24 h TTL) along with `crawlDelay`, and consult it before every fetch. Disallowed URLs are dropped.
- Use HTTP keep-alive and async I/O (epoll/Netty/asyncio), and set strict timeouts (connect 5 s, total 30 s) plus a max body size (e.g. 10 MB) so one slow server cannot hold a worker.

### 5.5 Crawler traps and quality

- Limit depth (a max of ~15-20 hops from a seed is a typical cap), URLs per host, and URL length (e.g. 2,000 chars).
- Detect repeating path segments (`/a/b/a/b/a/b`), calendar pages, session IDs.
- Per-host budget: stop after N pages unless the host has high priority.
- Content-hash dedup also catches traps that generate different URLs with the same page.

### 5.6 Freshness and extensions

- **Re-crawl:** keep `lastFetched` and an estimated change rate per URL, and re-enqueue with higher priority for fast-changing pages (news home pages). Use `If-Modified-Since`/ETag to save bandwidth.
- **JS-rendered pages:** a separate pool running headless Chromium, used only when the static HTML looks empty. It is 10–50x more expensive, so it must be isolated.
- **Other content types:** the parser stage dispatches on `Content-Type`, so adding PDFs or images is a new processor plus a new queue.
- **Multi-region:** crawl from regions close to the target hosts (less latency, fewer cross-region bytes), with each region owning a hash range of hosts.

## 6. What interviewers look for

- **Mid-level (~80% breadth):** a working high-level design (frontier, fetcher, parser, blob storage, metadata), basic robots.txt and politeness, general scaling intuition.
- **Senior (~60% breadth / 40% depth):** detailed politeness (crawl-delay, per-domain limits), clear bandwidth and machine-count math, queue trade-offs (SQS vs Kafka), retries and DLQ, proactively spots bottlenecks (DNS, dedup).
- **Staff+ (~40% breadth / 60% depth):** real depth in 3+ areas (queueing, rate limiting, dedup, DNS), practical experience behind each choice, original ideas (multiple DNS providers, front/back frontier queues, simhash, trap detection). The interviewer should learn something.

## 7. Common pitfalls

- A single queue with no per-host throttling, which gets the crawler banned
- Using a database lookup for every URL-seen check
- Forgetting `robots.txt`, DNS caching or crawler traps
- Treating a failed fetch as success or as permanent, with no retry policy or dead-letter queue
- Putting JS rendering on the hot path for every page
