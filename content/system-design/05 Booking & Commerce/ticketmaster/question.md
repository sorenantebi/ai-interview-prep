---
video: https://www.youtube.com/watch?v=fhdPyoO6aXI
topic: "Booking & Commerce"
difficulty: Medium
problem: "Ticketmaster"
---
# Design Ticketmaster (Event Ticket Booking)

**Topic:** Booking & Commerce · **Difficulty:** Medium · **Answer:** Ticketmaster - Solution

## Prompt

Design a ticket-booking platform like Ticketmaster. Users browse and search for events, view a seat map, pick seats and buy tickets. Each seat can be sold to exactly one person, and a popular concert can have millions of fans trying to buy at the same second.

## Requirements to pin down (ask the interviewer)

- Core flows: view an event, search for events, book tickets. Are booking history, admin event creation and dynamic pricing in scope (assume not)?
- Are seats numbered (reserved seating) or general admission?
- Do we hold seats while the user pays? For how long?
- Is payment in scope or can we assume a provider? Do we need a waiting room for hot events?
- Which paths need strong consistency (booking) and which favor availability (view/search)?

## Scale hints

- Read-heavy: roughly **100:1 reads to bookings**
- A hot event: up to ~10M concurrent users chasing ~50K seats; on-sale spikes are ~100x normal traffic
- Search latency target: **< 500 ms**
- Browsing/search can be eventually consistent; **booking must never double-sell a ticket**
- Seat map should refresh within a few seconds so users do not click dead seats

## Think about before opening the answer

1. What are the core entities (event, venue, performer, ticket, booking), and which APIs does the booking flow need (reserve, then confirm)?
2. How do you stop two people from buying the same ticket, and what do you do while the user is typing a card number?
3. What happens to a reserved ticket when the user abandons the checkout?
4. How do you scale view and search reads, and how do you speed up and cache search over events?
5. How do you protect the system and keep things fair (and the seat map live) when 10M users hit one event?
6. Which parts of the system need strong consistency and which can be cached or eventually consistent?

## Self-check

- [ ] I can design a ticket reservation with a TTL and explain what happens on expiry and on payment failure
- [ ] I can compare a status field plus cron, pessimistic locking and a distributed lock with TTL for tickets
- [ ] I can explain a virtual waiting room and why it beats just adding more servers
- [ ] I can separate the read-heavy browse path from the write-critical booking path
