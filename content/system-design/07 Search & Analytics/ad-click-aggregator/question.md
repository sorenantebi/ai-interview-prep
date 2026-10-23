---
video: https://www.youtube.com/watch?v=Zcv_899yqhI
topic: "Search & Analytics"
difficulty: Hard
problem: "Ad Click Aggregator"
---
# Design an Ad Click Aggregator

**Topic:** Search & Analytics · **Difficulty:** Hard · **Answer:** Ad Click Aggregator - Solution

## Prompt

Design a system that collects ad click events from a very large number of users, aggregates them, and lets advertisers query click metrics for their ads (e.g. clicks per ad per minute, per day). The numbers feed billing, so accuracy matters.

## Requirements to pin down (ask the interviewer)

- What is the finest time granularity advertisers need (1 minute? 1 hour)?
- How fresh must the dashboard be: seconds, minutes?
- Do we only count clicks, or also impressions and conversions?
- What dimensions can be queried: ad, campaign, country, device?
- How strict is correctness: is losing or double-counting a click acceptable, and is the data used for billing?
- Do we need to detect fraud / bot clicks, or is that out of scope?
- Must repeated clicks on the same ad shown to the same user be counted, and how do we tell a retry from a genuine new click?

## Scale hints

- ~10M active ads; ~10K clicks per second at peak (~1K/s average, ~100M clicks/day), with bursts above that for big events
- Raw events are large in total, but aggregated data is retained for years
- A single popular ad can receive a large share of the traffic
- Advertiser queries should return in well under a second

## Think about before opening the answer

1. What is stored raw and what is stored aggregated, and why keep both?
2. How do you make sure a click is never counted twice (retries, duplicates, forged clicks) and never lost?
3. Where does the aggregation happen, and what is the window?
4. How do you handle a single ad ID that generates a huge share of the traffic?
5. How do you query "clicks in the last 7 days, per hour" fast?
6. What if the stream job has a bug and produced wrong numbers for a day?

## Self-check

- [ ] I can estimate events/s, daily storage and aggregated rows
- [ ] I can explain at-least-once plus idempotency vs exactly-once
- [ ] I can compare stream-only, batch-only and the combined (lambda-style) approach
- [ ] I can describe hot-key mitigation and late event handling
