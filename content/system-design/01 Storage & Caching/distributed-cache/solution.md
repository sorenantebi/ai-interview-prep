---
topic: "Storage & Caching"
difficulty: Hard
problem: "Distributed Cache"
---
# Design a Distributed Cache – Solution

**Topic:** Storage & Caching · **Difficulty:** Hard · **Question:** Distributed Cache - Question

## 1. Requirements

**Functional**
- `GET(key)`, `SET(key, value, ttl?)`, `DELETE(key)`
- Per-key TTL and bounded memory with automatic eviction
- Horizontal scaling: add/remove nodes online

**Non-functional**
- Low latency: sub-ms server-side p99, one network hop for most requests
- High availability: survive node and AZ loss without a full outage
- Scale: ~1M-5M ops/s, ~10 TB hot data
- Eventual consistency is acceptable; the cache is not the source of truth

**Out of scope:** rich data structures, transactions, strong durability, multi-tenant billing.

## 2. Back-of-envelope

- 10 TB hot data; machines with 64 GB of usable RAM (leave headroom for fragmentation, buffers, fork/snapshots) → 10 TB / 64 GB ≈ **160 primaries**. With 1 replica each ≈ **320 nodes**.
- Load per primary: 5M ops/s / 160 ≈ 31K ops/s, well inside what one single-threaded Redis-class node handles (~100K ops/s). Capacity is bound by **memory**, not CPU.
- Network: 5M ops/s × ~5 KB ≈ 25 GB/s cluster-wide, ~150 MB/s per node. Fine for 10-25 Gbps NICs, but it is why we avoid proxy hops that double traffic.
- Key overhead: ~50-100 B of metadata per key. With 1 KB values 10 TB is ~10B keys; with 100 B values per-key overhead dominates, so mention memory efficiency.

## 3. Core entities and API

Entities: `Entry { key, value, expiresAt, lastAccess/frequency }`, `Slot` (a hash range), `Shard { slotRange, primary, replicas[] }`, `ClusterConfig { epoch, shards[] }`.

```
GET key                  -> value | miss
SET key value [EX ttl]   -> OK
DEL key                  -> count
```
Clients also receive a **slot map** (`slot → node`), refreshed through the cluster manager or via redirect responses (`MOVED slot node`).

## 4. High-level design

!Distributed Cache - Diagram.excalidraw

- **Routing:** `slot = CRC16(key) mod 16384`. A smart client library (or thin proxy) caches the slot map and sends each request directly to the owning primary: one hop.
- **Shards:** each shard has a primary taking reads/writes and one or two replicas copying asynchronously. Replicas give failover and can serve stale-tolerant reads.
- **Cluster manager:** etcd/ZooKeeper, or a gossip protocol between the nodes themselves, holds membership and the slot map, detects failures and orchestrates failover and resharding.
- **Usage:** the application does cache-aside: read the cache, on miss read the DB and populate.

## 5. Deep dives

### 5.1 Partitioning: which node owns a key?

| Approach | Pros | Cons |
|---|---|---|
| `hash(key) mod N` | Trivial | Changing N remaps almost every key: mass cache miss, DB meltdown |
| Consistent hashing ring + virtual nodes | Adding/removing a node moves only ~1/N of keys; vnodes even out load | Ring state to distribute, uneven loads with few vnodes, harder per-range operations |
| **Fixed hash slots (16,384) mapped to nodes** | Rebalance by moving whole slots, easy to track and migrate, explicit map | A slot map to distribute; slot count caps cluster size (fine at ~1K nodes) |

Recommended: **fixed slots** (Redis Cluster style); mention consistent hashing as the classic alternative (Memcached clients, Dynamo). Resharding: assign slots to a new node, migrate keys slot by slot while serving: `GET` on a migrating slot checks the source first and uses an `ASK` redirect to the target if the key has moved. New writes go to the target.

### 5.2 Replication and failover

- Primary → replicas by **asynchronous** replication of a command stream with an offset. Sync replication would add network RTT to every write, and a cache can tolerate losing the last few ms of writes.
- Failure detection: nodes ping each other; a node is marked **PFAIL** by one observer, **FAIL** once a majority of primaries agree. This quorum avoids false positives from a single flaky link.
- Promotion: the replica with the highest replication offset wins an election, gets a new **epoch** (config version) and takes over the slots. Other replicas re-attach to it; clients pick up the new slot map via `MOVED` or a watch.
- **Split brain:** a partitioned old primary may keep accepting writes. Mitigation: a primary that cannot reach a majority stops accepting writes after a timeout, and epochs make the highest one win. Writes accepted by the minority side are lost; acceptable for a cache, and the reason this is not a durable store.

!Distributed Cache - Deep Dive Diagram.excalidraw

### 5.3 Eviction and expiry

- Memory is bounded (`maxmemory`). Policies: **LRU** (good default for recency-skewed access), **LFU** (better for scan resistance: a one-off table scan doesn't flush hot keys), random, or TTL-first.
- Exact LRU needs a linked list and locking per access. Production systems use **approximate LRU/LFU**: sample ~5 random keys, evict the worst. Memcached uses segmented LRU with slab allocation.
- TTL expiry: **lazy** (check on access) plus **active** (a background loop samples keys with TTLs and deletes expired ones several times a second). Scanning all keys would be O(N), so sampling is the trick. Jitter TTLs (±10%) so a batch of keys written together doesn't expire together.
- Memory management: slab/size-class allocators or jemalloc limit fragmentation; monitor `used_memory_rss / used_memory`.

### 5.4 Hot keys and stampedes

| Problem | Mitigation |
|---|---|
| One key gets 100K+ ops/s, saturating one node | Client-side **L1 in-process cache** with seconds of TTL; replicate the hot key to multiple nodes and let clients pick randomly; split into `key#0..k` and fan reads |
| Cache stampede: popular key expires, thousands of requests hit the DB | **Request coalescing / single-flight**, a short lock (`SET NX`) so one caller recomputes, **stale-while-revalidate**, or probabilistic early refresh |
| Cold start / mass miss after node loss | Gradual warm-up, rate-limit DB fallback, prefer replica promotion over a fresh empty node |
| Cache penetration (nonexistent keys) | Cache negative results with a short TTL; a Bloom filter in front of the DB |

Detecting hot keys: sample traffic on each node (top-k counters) and report to the manager, which can push a "hot" flag to clients.

### 5.5 Consistency and write patterns

- **Cache-aside** (default): app reads cache, falls back to DB, writes cache. On update, **invalidate** (DELETE) rather than update in place, which avoids races where two writers apply updates out of order.
- **Write-through:** write to DB and cache together; no stale reads, but write latency rises and the cache fills with never-read data.
- **Write-back:** cache absorbs writes and flushes later; fastest, but data can be lost on crash. Only with durable replication and rarely appropriate here.
- Residual race: reader fetches old value from DB, writer updates DB and deletes the cache, reader then writes the old value. TTLs bound the staleness; versioned values or leases (Memcached "lease" tokens) close the gap.

### 5.6 Operations and clients

- **Smart client vs proxy** (mcrouter/Envoy/twemproxy): smart clients save a hop and scale with the client fleet but need a library in every language; a proxy centralizes routing, pooling and failover logic at the cost of latency (~100-300 µs) and a fleet to run.
- Connection pooling and pipelining reduce RTT cost; timeouts must be tight (a cache that is slow is worse than a miss) with a circuit breaker to the DB fallback.
- Optional persistence: periodic snapshots (RDB) or append-only log to speed restart; not required for correctness.
- Multi-region: independent cache per region, invalidations propagated through a message bus; do not synchronously replicate caches across regions.
- Metrics: hit ratio, evictions/s, memory fragmentation, replication lag, p99 latency, hot-key top-k.

## 6. What interviewers look for

- **Junior:** key → node hashing, replication for availability, LRU/TTL.
- **Mid:** consistent hashing or slots with reasoning on remapping, cache-aside and invalidation, failover.
- **Senior:** quorum failure detection and epochs, split-brain behavior, slot migration without downtime, approximate eviction and TTL sampling, hot-key and stampede mitigations, smart client vs proxy trade-offs, capacity math.

## 7. Common pitfalls

- `hash mod N` with no plan for resizing
- Synchronous replication on every write (kills latency) or no replicas at all
- Treating the cache as durable and losing the DB as source of truth
- Ignoring hot keys: balanced slots do not mean balanced load
- Updating the cache in place instead of invalidating
- Identical TTLs, which lead to synchronized expiry and stampedes
