---
video: https://www.youtube.com/watch?v=lsKU38RKQSo
topic: "Location & Marketplace"
difficulty: Hard
problem: "Uber"
---
# Design Uber (Ride Hailing)

**Topic:** Location & Marketplace · **Difficulty:** Hard · **Answer:** Uber - Solution

## Prompt

Design a ride-hailing service like Uber. A rider enters a destination and sees a fare and ETA estimate. After confirming the fare and requesting the ride, the system matches the rider with a nearby available driver, who can accept or decline and is then navigated to the pickup. Both sides then see live trip progress until the ride ends.

## Requirements to pin down (ask the interviewer)

- Only standard rides, or also pooling, scheduled rides, ratings and multiple vehicle types (X / XL / Comfort)?
- Do we compute routes/ETAs ourselves or can we call a maps/routing service?
- Is payment, driver onboarding and surge pricing in scope, or only request-to-match-to-trip?
- How strict must matching be: is it acceptable for a driver to briefly be offered two rides?

## Scale hints

- ~1M drivers online at peak, each sending a GPS update every ~4-5 seconds
- ~20M rides/day, with strong city-level and rush-hour peaks
- Match a rider to a driver quickly: within about a minute, otherwise report failure
- A driver must never be assigned to two rides at once (strong consistency)
- A burst of ~100K concurrent ride requests from one location (stadium letting out)

## Think about before opening the answer

1. What are the core entities, and which of them change thousands of times per second?
2. How do you store and query "available drivers near this point" with constantly moving data?
3. How do you avoid sending the same driver to two riders, and what if the driver does not answer?
4. Which parts need durable storage, and which are fine to lose on a crash?
5. How do you push offers and live location to phones reliably, and how do you cut the cost of constant pings?
6. What if the request spike or a worker crash loses ride requests, or the chosen driver never responds?
7. What happens at a stadium letting out, or when a whole region fails over?

## Self-check

- [ ] I can estimate location write QPS and explain why it does not belong in the main database
- [ ] I can compare at least 3 geospatial indexing options (geohash, quadtree, H3, Redis GEO)
- [ ] I can describe the matching flow with locking, timeouts and retries
- [ ] I can model the ride lifecycle as a state machine and say where its state lives
