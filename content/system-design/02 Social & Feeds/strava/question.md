---
topic: "Social & Feeds"
difficulty: Medium
problem: "Strava"
---
# Design Strava

**Topic:** Social & Feeds · **Difficulty:** Medium · **Answer:** Strava - Solution

## Prompt

Design a fitness tracking social network. Athletes record runs and rides on a phone or watch (GPS track, time, heart rate), upload them, and see stats and a map. Athletes follow each other and see friends' activities in a feed. Popular stretches of road or trail are defined as segments, and every athlete who rides or runs a segment gets ranked on its leaderboard.

## Requirements to pin down (ask the interviewer)

- Is live tracking in scope, or only upload after the activity finishes?
- What data does an activity contain (GPS rate, sensors), how large, and must the app work offline?
- Are segments user-created? How many, and how precisely must matching work?
- Which leaderboards: all-time, this year, friends, age group, with filters?
- Privacy: hidden start/end zones, private activities, follower-only visibility?

## Scale hints

- ~100M registered athletes, ~5M new activities per day
- A 1-hour activity at 1 Hz GPS is ~3,600 points
- Tens of millions of segments worldwide; each activity may touch dozens
- Feed and leaderboard reads are far more frequent than uploads

## Think about before opening the answer

1. What are the entities and the upload API? How do large GPS files reach storage on unreliable connections?
2. Why should processing (stats, segment matching) be asynchronous, and what do users see meanwhile?
3. How do you find which segments an activity passed through without comparing against all segments?
4. How do you keep and serve a leaderboard for a segment with a million efforts?
5. How do you build the activity feed, and does the fan-out problem apply?
6. How do you handle re-processing when the matching algorithm improves or a segment changes?

## Self-check

- [ ] I can estimate GPS storage per day and per year
- [ ] I can explain geospatial indexing (geohash/S2) used for candidate segment lookup
- [ ] I can design a Redis sorted-set leaderboard and its persistence
- [ ] I can make the processing pipeline idempotent and re-runnable
