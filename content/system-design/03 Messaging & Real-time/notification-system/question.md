---
topic: "Messaging & Real-time"
difficulty: Medium
problem: "Notification System"
---
# Design a Notification System

**Topic:** Messaging & Real-time · **Difficulty:** Medium · **Answer:** Notification System - Solution

## Prompt

Design a platform-wide notification service. Internal services (orders, social, marketing, security) ask it to notify users, and it delivers messages through mobile push, email and SMS, respecting user preferences, without sending duplicates and without overloading downstream providers.

## Requirements to pin down (ask the interviewer)

- Which channels: push, email, SMS, in-app? Any priority levels (e.g. OTP vs newsletter)?
- Do we need scheduled and bulk/broadcast notifications?
- Do users have opt-out preferences and quiet hours? Templates and localisation?
- Do we need delivery tracking (sent, delivered, opened) and is a rare duplicate acceptable?

## Scale hints

- ~10M notifications per day average, with **bursts of 1M+ in a few minutes** (flash sale, breaking news)
- Time-critical messages (OTP, security alerts) must go out within seconds
- Third-party providers (APNs/FCM, SES, Twilio) are rate limited and can fail

## Think about before opening the answer

1. What is the API between producer services and the notification system?
2. Why put a queue in the middle, and how many queues would you use?
3. How do you stop a user from receiving the same notification twice when a retry happens?
4. How do you keep an email blast from delaying an OTP?
5. What do you do when a provider is slow or down?
6. Where do user preferences and templates live, and how are they kept off the hot path?

## Self-check

- [ ] I can draw a decoupled, queue-based pipeline with per-channel workers
- [ ] I can explain idempotency, retries with backoff and a dead-letter queue
- [ ] I can describe priority isolation and rate limiting
- [ ] I can say what is persisted for tracking and for how long
