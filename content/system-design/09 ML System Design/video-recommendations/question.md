---
video: https://www.youtube.com/watch?v=GncgOIiMII8
topic: "ML System Design"
difficulty: Hard
problem: "Video Recommendations"
---
# Design Video Recommendations ("Up Next")

*The embedded video covers recommendation-system infra basics, not a full walkthrough of this problem.*

**Topic:** ML System Design · **Difficulty:** Hard · **Answer:** Video Recommendations - Solution

## Prompt

Design the recommendation system behind a YouTube-style "up next" panel. While a user watches a video, the system picks a handful of videos to suggest next, drawn from a huge catalog, so that the user keeps watching content they actually enjoy.

## Requirements to pin down (ask the interviewer)

- Which surface: "up next" while watching, the homepage feed, or both?
- How many slots are shown at once (5? 10?) and what is the latency budget?
- What counts as success for the business: clicks, watch time, satisfaction, creator health?
- Which signals do we have: explicit (likes, subscriptions, "not interested") vs implicit (watch time, shares, returns)?

## Scale hints

- ~1B videos in the catalog, ~1B daily active users
- ~5 recommendations rendered per request
- End-to-end budget around 250 ms per request
- You cannot score every video for every request: plan for a funnel

## Think about before opening the answer

1. Why is raw CTR a dangerous business objective, and what would you pick instead?
2. How do you turn the business objective into an ML objective (ranking + multiple predicted engagements + a value model)?
3. What does the multi-stage funnel look like, and what does each stage optimize (recall vs precision)?
4. Which labels and features would you use, and which ones can be cached vs must be fresh?
5. Baseline vs stronger heavy ranker: MLP, DLRM, or a transformer sequence model?
6. How do you train retrieval embeddings (two-tower, negatives)?
7. How do you evaluate offline and online, and what can mislead you (position bias, novelty effects)?
8. How do you handle cold start, feedback loops and explore/exploit?

## Self-check

- [ ] I can justify a business objective better than CTR and map it to an ML objective
- [ ] I can draw candidate generation → light ranker → heavy ranker → re-ranking with rough set sizes
- [ ] I can explain two-tower retrieval with hard negatives and a multi-task heavy ranker
- [ ] I can name offline and online metrics and at least two sources of bias in the training data
