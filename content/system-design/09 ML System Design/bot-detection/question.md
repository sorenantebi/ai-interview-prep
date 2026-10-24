---
video: https://www.youtube.com/watch?v=wI4L11EoW3I
topic: "ML System Design"
difficulty: Medium
problem: "Bot Detection"
---
# Design Bot Detection

**Topic:** ML System Design · **Difficulty:** Medium · **Answer:** Bot Detection - Solution

## Prompt

Design a system that detects bot accounts on a social media platform. Bots create fake accounts, spam friend requests and messages, post duplicate or harmful content and spread misinformation. The goal is to separate legitimate user activity from automated or malicious activity and limit the damage bots do to real users.

## Requirements to pin down (ask the interviewer)

- How prevalent are bots, before and after existing simple heuristics?
- What happens when a real user is wrongly flagged? Is there an appeals process, and what does it cost?
- How fast must we catch a bot (at signup, after first actions, within a day)?
- Are there known tell-tale signs, and how quickly do bot authors adapt?
- Do we have ground-truth labels? Who produces them and at what rate?
- Which actions can we take: ban, demote, rate-limit?

## Scale hints

- ~500M DAU, 1-2 sessions each, so billions of actions per day
- Unchecked, bots can be 50%+ of actions; basic heuristics bring that below ~1%
- Human investigators can label only a few hundred accounts per week
- Adversarial: the attackers retrain against whatever we ship

## Think about before opening the answer

1. What business objective captures "bots hurt users" better than "number of bots banned"?
2. With only hundreds of trusted labels a week, where do you get more training signal?
3. Which feature families are hardest for a bot to fake (timing, graph) vs easiest (content)?
4. Why is a large content-focused multi-modal model the wrong tool here? What would you use instead?
5. How do you catch bots you have never seen before (unknown unknowns)?
6. How do you keep inference cheap at billions of actions per day, and when do you re-score an account?
7. How do you calibrate and evaluate when labels are scarce and the distribution keeps drifting?

## Self-check

- [ ] I can explain the adversarial dynamics (drift, survivorship bias, positive suppression) and how holdouts help
- [ ] I can sketch a graph + sequence model and justify GraphSAGE and a GRU
- [ ] I can describe self-supervised pretraining that makes a few labels go a long way
- [ ] I can compare calibration methods and anomaly detectors (isolation forest vs autoencoder)
