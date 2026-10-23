---
topic: "Social & Feeds"
difficulty: Medium
problem: "News Aggregator"
---
# Design a News Aggregator

**Topic:** Social & Feeds · **Difficulty:** Medium · **Answer:** News Aggregator - Solution

## Prompt

Design a news aggregator like Google News. The system continuously collects articles from thousands of publishers, groups articles about the same event, and presents readers with a fresh, browsable feed organized by topic, region and relevance. Readers can click through to the publisher's site.

## Requirements to pin down (ask the interviewer)

- How many sources, and do they offer RSS/Atom feeds or must we scrape HTML?
- Do we show full article text or only title, snippet and thumbnail with a link out?
- How fast must breaking news appear after a publisher posts it?
- Is the feed personalized, or the same top stories per topic and region for everyone?
- Do we need search, and do we need to group duplicate or similar stories into one cluster?

## Scale hints

- ~100K sources, ~10M articles fetched per day (many are near-duplicates)
- ~50M daily readers, ~10 feed loads each, heavily read dominated
- Breaking news should show up within 1 to 2 minutes
- Feed latency target < 200 ms

## Think about before opening the answer

1. What are the entities and the two main flows (ingest and read)?
2. How do you crawl 100K sources politely and keep fresh sources fresher than stale ones?
3. How do you detect that 300 articles describe the same event?
4. How do you rank stories, and where is the ranking computed?
5. What do you cache, and how do you handle a sudden traffic spike on a big story?
6. How do you stay correct when a publisher is slow, sends bad HTML, or republishes the same article?

## Self-check

- [ ] I can size crawl rate, storage and read QPS
- [ ] I can compare polling, WebSub/push and sitemaps for freshness
- [ ] I can describe exact versus near-duplicate detection (hashing, SimHash, embeddings)
- [ ] I can separate the ingest pipeline from the serving path and justify each store
