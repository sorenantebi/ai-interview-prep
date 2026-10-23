---
topic: "Fintech"
difficulty: Hard
problem: "Robinhood"
---
# Design Robinhood (Retail Stock Trading App)

**Topic:** Fintech · **Difficulty:** Hard · **Answer:** Robinhood - Solution

## Prompt

Design a retail stock trading app like Robinhood. Users see live stock prices and charts, maintain watchlists, place buy/sell orders, and see their portfolio and order status. Orders are routed to external brokers, market makers or exchanges, which execute them and report back fills.

## Requirements to pin down (ask the interviewer)

- Which order types: market, limit, stop? Fractional shares? Extended hours?
- Do we execute orders ourselves (clearing/broker-dealer) or forward to a market maker/exchange?
- How real-time must quotes be (every tick, or throttled to 1/s per symbol per user)?
- How is money handled: instant buying power from deposits, margin, settlement (T+1)?

## Scale hints

- ~20M users, ~5M concurrently online at market open; ~10K symbols
- Market data: tens of thousands of ticks per second across the market, bursts of 100K+/s at open
- Orders: ~1M/day average, 10x spikes during market events; every order must be traceable
- Live quote latency to the client: < 1 s; order acknowledgement < 500 ms

## Think about before opening the answer

1. What are the core entities and APIs (quotes, watchlist, orders, portfolio)?
2. How do you fan out prices for 10K symbols to millions of connected clients efficiently?
3. How do you ensure a user cannot spend money or sell shares they do not have, even with concurrent orders?
4. What is the lifecycle of an order, and how do you handle partial fills, cancels and an exchange that does not answer?
5. How do you avoid sending the same order to the exchange twice after a crash or retry?
6. Which data needs strong consistency and which can be eventually consistent?

## Self-check

- [ ] I can design a market data fan-out path (ingest, pub/sub, WebSocket) with conflation
- [ ] I can design an order state machine with idempotent routing and fill handling
- [ ] I can protect buying power and share positions against concurrent orders
- [ ] I can describe reconciliation with the broker/clearing house at end of day
