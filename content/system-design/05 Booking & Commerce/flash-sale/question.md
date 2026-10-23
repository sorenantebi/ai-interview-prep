---
topic: "Booking & Commerce"
difficulty: Hard
problem: "Flash Sale"
---
# Design a Flash Sale System

**Topic:** Booking & Commerce · **Difficulty:** Hard · **Answer:** Flash Sale - Solution

## Prompt

Design the backend for a flash sale on an e-commerce site: at a fixed time (say 12:00:00) a limited stock of a product (e.g. 10,000 units of a discounted console) goes on sale. Millions of users hit "Buy" within seconds. The system must never oversell, must stay up under the spike, and should be as fair as possible.

## Requirements to pin down (ask the interviewer)

- One product or many concurrent flash items? How many units per user?
- Is payment synchronous, or can we reserve stock first and let the user pay within N minutes?
- Is it acceptable to tell most users "sold out" quickly? What fairness do we need (random vs first-come-first-served)?
- Bots and scalpers: how much do we need to defend against them?

## Scale hints

- 5M to 10M users waiting for the sale; ~1M requests per second at peak for a few seconds
- Stock: 10K to 100K units, so >99% of requests must be rejected cheaply
- Zero overselling; no unit may be sold twice or lost forever
- Rest of the shop (browse, other products) must stay healthy during the spike

## Think about before opening the answer

1. Where should the stock counter live, and how do you decrement it atomically at this rate?
2. Why can't the database handle `UPDATE stock = stock - 1` for every request, and what do you do instead?
3. How do you filter out 99% of traffic before it reaches your core services?
4. What happens if a user reserved a unit but never pays, or if payment fails?
5. How do you make "buy" idempotent so double clicks and retries do not create two orders?
6. How do you prevent bots and one user from grabbing many units?

## Self-check

- [ ] I can design a layered funnel: CDN, rate limit, waiting room, in-memory stock gate, async order creation
- [ ] I can explain an atomic Redis stock decrement (Lua) and what to do when Redis fails
- [ ] I can reconcile Redis stock with the DB and release unpaid reservations
- [ ] I can state which consistency guarantees we need and where we trade them away
