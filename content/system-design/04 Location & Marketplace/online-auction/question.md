---
video: https://www.youtube.com/watch?v=o8nSXW-B7Rw
topic: "Location & Marketplace"
difficulty: Medium
problem: "Online Auction"
---
# Design an Online Auction (eBay-style)

**Topic:** Location & Marketplace · **Difficulty:** Medium · **Answer:** Online Auction - Solution

## Prompt

Design an online auction platform. Sellers list an item with a starting price and an end time. Buyers place bids; a bid must be higher than the current highest bid. Everyone watching the auction sees the current price update in near real time. When the auction ends, the highest bidder wins.

## Requirements to pin down (ask the interviewer)

- Plain ascending auctions only, or also proxy/auto-bidding and "buy it now"?
- Is the price update expected to be instant (push) or is polling acceptable?
- What happens if a bid arrives in the last seconds: is there anti-sniping extension?
- Is payment in scope, or do we stop at determining the winner?

## Scale hints

- ~10M active auctions, ~1M new auctions/day
- Typical auction has a handful of bids, but a popular one can see thousands of bids/minute near its end
- ~100K concurrent viewers on the hottest auctions
- Bid acknowledgement < 200 ms; auctions must close within about a second of the deadline

## Think about before opening the answer

1. What are the entities and the APIs, and which one is the hardest to make correct?
2. Two people bid the same amount at the same instant. How does the system decide?
3. How do you push price changes to thousands of watchers without hammering the DB?
4. How do you close an auction reliably at an exact time across many servers?
5. What if the client retries a bid, or a server crashes after accepting it?
6. How do you keep a very hot auction from becoming a bottleneck?

## Self-check

- [ ] I can write the check that accepts or rejects a bid atomically
- [ ] I can compare optimistic locking, row locks and a single-writer-per-auction design
- [ ] I can describe real-time fan-out with WebSocket/SSE and pub/sub
- [ ] I can explain how auction closing works and how it stays correct under failures
