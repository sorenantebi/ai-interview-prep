---
video: https://www.youtube.com/watch?v=LjLx0fCd1k8
topic: "Messaging & Real-time"
difficulty: Hard
problem: "FB Live Comments"
---
# Design FB Live Comments (Live Video Comment Stream)

**Topic:** Messaging & Real-time · **Difficulty:** Hard · **Answer:** FB Live Comments - Solution

## Prompt

Design the comment feature for a live video broadcast. Viewers post comments while watching, and every other viewer of the same video sees new comments appear within a second or two. A late joiner should see recent comments, and older comments should be browsable.

## Requirements to pin down (ask the interviewer)

- Are comments only text? Replies/threads, reactions (assume out of scope)?
- Must a viewer see new comments in near real time, and also the comments posted before they joined?
- Is ordering strict, or is "roughly chronological" enough? Availability vs consistency?
- Must every viewer see every comment, or can we sample when a stream is very busy?
- Is moderation/security in scope (assume not)?

## Scale hints

- Millions of concurrent live videos, most with few viewers
- A viral stream can have **~1M+ concurrent viewers** and thousands of comments per second (a "mega-stream" is ~5K comments/s)
- Comment latency target: visible to other viewers in **< 200 ms** end to end
- Read path (delivery) is hugely larger than the write path; a single server can hold ~100K+ connections

## Think about before opening the answer

1. Why is polling a bad fit here, and what are your options for server push (SSE vs WebSocket)? Which direction needs which?
2. How does a comment posted on one server reach viewers of the same video connected across many other servers?
3. What is your pub/sub design, and what is the key of a channel?
4. Which parts of the system can be lossy, and which cannot?
5. How do you serve history to a user who joins mid-stream?
6. What happens when a single video becomes a hot key (a mega-stream), and what do you do when a viewer's connection drops?

## Self-check

- [ ] I can justify SSE vs WebSocket for this specific read/write imbalance
- [ ] I can explain a fan-out design that scales to one very hot video
- [ ] I can design the comment store and its partition key
- [ ] I can describe graceful degradation (sampling, batching) under load
