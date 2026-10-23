---
topic: "Infrastructure & Scheduling"
difficulty: Medium
problem: "Job Scheduler"
---
# Design a Distributed Job Scheduler

**Topic:** Infrastructure & Scheduling · **Difficulty:** Medium · **Answer:** Job Scheduler - Solution

## Prompt

Design a job scheduling service (think cron-as-a-service, or the scheduler behind a workflow product). Users submit jobs that should run once at a specific time or repeatedly on a schedule. The system must run each job at (or very close to) its due time on a fleet of workers, even when machines fail.

## Requirements to pin down (ask the interviewer)

- One-off jobs, recurring (cron expression) jobs, or both? Delayed jobs ("in 10 minutes")?
- What does a job do: call an HTTP endpoint, run a container, run code in our workers? How long can it run?
- Delivery guarantee: at-most-once, at-least-once, or exactly-once? Is idempotency the user's problem?
- How precise must timing be (seconds? sub-second?). Priorities? Per-tenant fairness?
- Retries, timeouts, cancellation, visibility into job history?

## Scale hints

- ~100M scheduled jobs stored, ~10K jobs becoming due per second at peak
- Execution start within ~1-2 s of the due time at p99
- No job lost, and a worker crash must not strand a job

## Think about before opening the answer

1. What is the data model, and what index makes "find everything due now" cheap?
2. How do scheduler instances avoid running the same job twice, and how do they scale beyond one poller?
3. How do you detect a dead worker and recover its job without duplicating work?
4. How do you implement recurring schedules and retries with backoff?
5. What do you do about a thundering herd at the top of the minute, and about poison jobs?

## Self-check

- [ ] I can justify at-least-once plus idempotency instead of promising exactly-once
- [ ] I can explain claiming rows safely with a lease or `SKIP LOCKED`
- [ ] I can describe retry, backoff and dead-letter handling
- [ ] I can say how the scheduler itself scales and fails over
