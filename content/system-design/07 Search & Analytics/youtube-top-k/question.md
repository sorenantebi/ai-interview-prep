---
video: https://www.youtube.com/watch?v=y-tA2NW4LNY
topic: "Search & Analytics"
difficulty: Hard
problem: "YouTube Top K"
---
# Design YouTube Top K Videos

**Topic:** Search & Analytics · **Difficulty:** Hard · **Answer:** YouTube Top K - Solution

## Prompt

Design a system that returns the top K most-viewed videos for a time window (last hour, last day, last month, all time). Every video view generates an event, and users or dashboards request the ranking at any time.

## Requirements to pin down (ask the interviewer)

- Which windows are required (all time, 1 hour, 1 day, 1 month), and are they tumbling (aligned to the hour/day) or sliding?
- What is the maximum K, and is it a request parameter?
- Must the results be precise, or is an approximation acceptable?
- How stale may a result be (real-time, or about a minute behind)?
- What latency does the query need, and is this global only?

## Scale hints

- ~70B views per day, which is roughly 700K views/s
- ~3.6B videos in total (about 1M new videos/day over 10 years)
- Results must be precise, up to K = 1,000, with ~1 minute of acceptable delay and ~10 ms query latency
- The answer is tiny (K items) and changes slowly, but there are a few extremely hot videos

## Think about before opening the answer

1. Why is `SELECT video, COUNT(*) ... ORDER BY count DESC LIMIT K` not an option?
2. What data structure maintains a top-K, and why is a per-video counter in a database a bottleneck?
3. How do you scale the counting across many machines and still produce a correct global top K?
4. How do you handle ~700K writes/s on the database: sharding, batching, or both?
5. How do you answer 1 hour / 1 day / 1 month windows without scanning billions of rows?
6. How do you meet 10 ms latency, and what happens when a cached result expires?
7. What changes for sliding windows, and where would a Count-Min Sketch or a specialised database (TimescaleDB, Druid, Pinot, ClickHouse) fit?

## Self-check

- [ ] I can explain why partitioning by video ID makes local top-K merging exact
- [ ] I can design pre-aggregated window tables and bucketed roll-ups (minute -> hour -> day)
- [ ] I can compare exact counting (about 64 GB) with Count-Min Sketch (hundreds of MB) and say when each is acceptable
- [ ] I can separate the write path (counting) from the read path (cached top-K)
