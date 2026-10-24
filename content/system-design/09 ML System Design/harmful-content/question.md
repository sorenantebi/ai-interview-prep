---
video: https://www.youtube.com/watch?v=9KUC_nHydZg
topic: "ML System Design"
difficulty: Medium
problem: "Harmful Content Detection"
---
# Design Harmful Content Detection

**Topic:** ML System Design · **Difficulty:** Medium · **Answer:** Harmful Content Detection - Solution

## Prompt

Design the ML system that moderates posts on a large social network like Facebook. Posts can carry text and images (and video, which you may scope out). The system should find harmful posts, from nudity and violence up to terrorism and trafficking, and decide what to do with them: remove, demote, or send to a small human review team.

## Requirements to pin down (ask the interviewer)

- Which modalities are in scope (text, images, video)? Posts only, or comments too?
- Which actions are available (auto-remove, demote, human review)? How much reviewer capacity is there?
- How costly is a false positive (wrongly removed post) vs a false negative (harmful post stays up)? Is there a precision bar for automatic removal?
- How fast must we act? Is it fine to re-score a post later as more signal arrives?
- Do we have labelled data, or is this a cold start?

## Scale hints

- ~1B new posts per day
- Harmful content is rare (< 1% of posts), but that is still millions per day
- Auto-removal only when we are at least ~95% confident (precision guardrail)
- Starting labels: ~50k examples, balanced 50/50 harmful vs benign

## Think about before opening the answer

1. What is the business objective, and why is "accuracy" or "max content removed" a poor choice?
2. Beyond the labelled set, what other (noisier, larger) sources of supervision exist on a social network?
3. Which feature families matter: content, audience behaviour, creator? Which are only available after the post goes live?
4. How do you combine text, images and tabular features in one model (separate models vs late fusion vs multi-modal transformer)?
5. How do you afford a heavy model on 1B posts/day, and when do you re-score a post?
6. How do you evaluate offline and online when positives are < 1% of traffic?

## Self-check

- [ ] I can state a business objective with a precision guardrail and explain why it is better than the alternatives
- [ ] I can explain how class imbalance and view-weighting shape the loss
- [ ] I can describe a two-stage (cheap filter → heavy model) inference cascade with re-triggering
- [ ] I can name offline metrics (PR-AUC, Recall@Precision) and an online labelling strategy (importance sampling)
