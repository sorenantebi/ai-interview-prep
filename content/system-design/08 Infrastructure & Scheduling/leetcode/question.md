---
video: https://www.youtube.com/watch?v=1xHADtekTNg
topic: "Infrastructure & Scheduling"
difficulty: Medium
problem: "LeetCode"
---
# Design LeetCode (Online Coding Judge)

**Topic:** Infrastructure & Scheduling · **Difficulty:** Medium · **Answer:** LeetCode - Solution

## Prompt

Design an online coding platform where users browse programming problems, write code in the browser, submit it in one of several languages, and get a verdict (Accepted, Wrong Answer, Time Limit Exceeded, ...) within seconds. The platform also hosts timed contests with a live leaderboard.

## Requirements to pin down (ask the interviewer)

- Which languages? Are resource limits (time, memory) per problem?
- Is "Run" (sample tests) different from "Submit" (full hidden tests)?
- Contest scoring rules: points, penalty time, ranking ties? Is the leaderboard live during the contest?
- Which features are in scope: problem list/detail, submit with fast feedback, live leaderboard? Authentication, profiles, payments, discussion forums and editorials are likely out of scope.
- How hostile do we assume the code is?

## Scale hints

- ~4,000 problems, ~100 test cases each; hundreds of thousands of users, ~5M submissions per day on a normal day
- A contest with ~100K concurrent participants: bursts of ~10K submissions at once, far above the normal peak
- Verdict latency target: ~5 seconds for typical problems

## Think about before opening the answer

1. How do you run untrusted code safely, and what isolation and limits do you apply?
2. Should the submission request run the code inline, or go through a queue? Why?
3. How do you scale the judging fleet for contest spikes, and keep results correct and consistent?
4. How is the contest leaderboard computed and served to 100K viewers (and why not query the DB on every poll)?
5. How are test cases stored and delivered to judge workers, and how do you keep them secret?
6. How can one test case definition work across all languages (inputs like trees or linked lists)?

## Self-check

- [ ] I can list at least four layers of sandboxing for untrusted code
- [ ] I can draw the asynchronous submit, queue, judge, verdict flow and the status polling
- [ ] I can compare running code on the API server vs VMs vs containers, and say why hardened containers win
- [ ] I can explain a leaderboard with Redis sorted sets and how it recovers from loss
- [ ] I can explain how to make judging deterministic and retry-safe
