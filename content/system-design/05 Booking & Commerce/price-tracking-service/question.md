---
topic: "Booking & Commerce"
difficulty: Medium
problem: "Price Tracking Service"
---
# Design a Price Tracking Service (CamelCamelCamel-style)

**Topic:** Booking & Commerce · **Difficulty:** Medium · **Answer:** Price Tracking Service - Solution

## Prompt

Design a service that tracks product prices on large e-commerce sites. Users paste a product link (or use a browser extension), see a price history chart, and set an alert such as "tell me when this drops below 50 EUR". The system keeps checking prices and notifies users when their condition is met.

## Requirements to pin down (ask the interviewer)

- Which retailers? Is there an official or affiliate API, or must we crawl HTML pages?
- How fresh must prices be (minutes, hours, daily)? Is it the same for every product?
- What alert types: absolute threshold, percent drop, all-time low? Which channels: email, push?
- Do we track only products that someone watches, or the whole catalog?

## Scale hints

- ~50M tracked products, ~10M users, ~100M active alerts
- Popular products refreshed every ~15 min; long-tail daily or weekly
- Thousands of price checks per second overall; retailers rate limit and block aggressive crawlers
- Price history: years of data per product, charts must load in < 500 ms

## Think about before opening the answer

1. What are the entities, and what is the minimal API (watch, history, alerts)?
2. How do you decide which products to fetch and how often, under a limited crawl budget?
3. How do you fetch at scale without being blocked, and what do you do with parse failures or layout changes?
4. How do you store price history compactly and serve charts quickly?
5. How do you match a new price against 100M alerts efficiently, without scanning them all?
6. How do you avoid duplicate or flapping notifications?

## Self-check

- [ ] I can design a priority-based crawl scheduler with per-domain politeness
- [ ] I can pick storage for time series vs relational alert data, and justify it
- [ ] I can design alert matching that is indexed by product and threshold
- [ ] I can explain deduplication of unchanged prices and notification idempotency
