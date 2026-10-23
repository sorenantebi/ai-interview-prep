---
video: https://www.youtube.com/watch?v=yz1jtze4qr8
topic: "Location & Marketplace"
difficulty: Medium
problem: "Yelp"
---
# Design Yelp (Local Business Search and Reviews)

**Topic:** Location & Marketplace · **Difficulty:** Medium · **Answer:** Yelp - Solution

## Prompt

Design a service like Yelp. Users search for businesses by keyword and location (e.g. "ramen near me" in a map area), open a business page, and read and write reviews with a 1-5 star rating. Search results are ranked by relevance and rating, and business ratings should update when new reviews arrive.

## Requirements to pin down (ask the interviewer)

- Search by name/category only, or free text and filters (price, open now, rating)?
- Is the map viewport or "radius around a point" the main query?
- Can a user review a business more than once? Are photos in scope?
- Do business owners edit their own data, and how fast must edits show up in search?

## Scale hints

- ~100M monthly users, ~10M businesses, ~500M reviews
- Search is the dominant traffic: roughly 100x more reads than new reviews
- Business data changes rarely; reviews arrive at a modest rate
- Search latency target: < 200 ms p95

## Think about before opening the answer

1. What are the entities and the 3 main APIs?
2. How do you find businesses within a radius and match text at the same time?
3. Do you need a geospatial index if you already have a search engine?
4. How do you keep the average rating correct without recomputing over millions of reviews?
5. How do you keep the search index in sync with the database of record?
6. What if a business has 100K reviews, or two reviews arrive at once from one user?

## Self-check

- [ ] I can estimate the size of the business and review datasets
- [ ] I can compare geohash, quadtree and a search-engine geo index for proximity search
- [ ] I can explain how the rating is updated incrementally and safely
- [ ] I can describe how data flows from the DB to the search index
