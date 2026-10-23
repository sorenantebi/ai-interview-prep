---
topic: "Storage & Caching"
difficulty: Hard
problem: "Distributed Cache"
---
# Design a Distributed Cache

**Topic:** Storage & Caching · **Difficulty:** Hard · **Answer:** Distributed Cache - Solution

## Prompt

Design a distributed, in-memory key-value cache (think Redis Cluster or Memcached at scale) used by hundreds of internal services. It stores data in RAM across many machines, serves `GET`, `SET` and `DELETE` with sub-millisecond latency, and keeps working when machines fail or when capacity is added.

## Requirements to pin down (ask the interviewer)

- Is it a pure cache (data can be lost and refetched) or a store with durability guarantees?
- Which operations: only get/set/delete with TTL, or also data structures (lists, counters)?
- Consistency expectations: is stale data acceptable? For how long?
- Single region or multi-region? How much isolation between tenants?
- Do clients talk to nodes directly (smart client) or via a proxy?

## Scale hints

- ~1M ops/s average, ~5M ops/s peak, reads : writes about 10 : 1
- Hot dataset ~10 TB, values mostly < 10 KB
- p99 latency < 1 ms on the server side, 99.99% availability
- Nodes fail routinely; capacity must grow and shrink without downtime

## Think about before opening the answer

1. How do you decide which node owns a key, and what happens to ownership when nodes join or leave?
2. What data survives a node crash, and what does failover look like?
3. How do you evict when memory is full, and how do you expire keys cheaply?
4. How do you handle a single extremely hot key that one node cannot serve?
5. Which caching pattern (aside, write-through, write-back) do you offer, and what are the consistency consequences?
6. What goes wrong when a whole node's keys vanish at once?

## Self-check

- [ ] I can compare mod-N, consistent hashing and fixed hash slots
- [ ] I can explain replication, failure detection and promotion
- [ ] I can explain LRU/LFU eviction and TTL expiry costs
- [ ] I can name at least three hot-key and stampede mitigations
