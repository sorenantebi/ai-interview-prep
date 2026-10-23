---
video: https://www.youtube.com/watch?v=18Fg5Akhkqw
topic: "Social & Feeds"
difficulty: Medium
problem: "Tinder"
---
# Design Tinder

**Topic:** Social & Feeds · **Difficulty:** Medium · **Answer:** Tinder - Solution

## Prompt

Design a location-based dating app. Users create a profile with preferences (age range, interests, maximum distance). The app shows a stack of nearby profiles one by one; the user swipes right (like) or left (pass). When two users have both liked each other, they match and are notified, and can then chat.

## Requirements to pin down (ask the interviewer)

- Which filters are needed: distance, age range, interests, others?
- Must a user never see the same profile twice (or at least not for a long time)?
- How strict is consistency for swipes: can a mutual like ever be missed? Is the match notification real-time? Are chat, photo upload and premium features in scope? (usually no)
- How fresh must a user's location be? Do users travel and change cities?
- Do we need ranking of candidates (attractiveness / activity) or only filtering?

## Scale hints

- ~20M daily active users, ~100 swipes per user per day (~2B swipes/day)
- Swipes are bursty: evenings and weekends peak at 4-5x average
- A user may have swiped on tens of thousands of profiles over time
- Candidate stack (feed) generation under ~300 ms
- Swiping must be strongly consistent; the match notification should arrive within a second or two

## Think about before opening the answer

1. What are the core entities and APIs?
2. How do you find "nearby users matching my filters" quickly? Which index, and how do you shard it?
3. How do you guarantee you never show a profile that was already swiped?
4. A match is mutual. How do you detect it on each swipe, and what happens if both users swipe at the same moment?
5. Where do you precompute work (candidate stacks) and where do you stay on demand?
6. What should be cached, and which data needs durability above all?
7. How do you keep a cached candidate stack from going stale when users move or change preferences?

## Self-check

- [ ] I can estimate swipe QPS and swipe storage per year
- [ ] I can compare geohash, S2/quadtree and Elasticsearch geo queries
- [ ] I can design the seen-profile filter (Bloom filter vs stored set) with trade-offs
- [ ] I can make match creation idempotent and race-free
