---
video: https://www.youtube.com/watch?v=cr6p0n0N-VA
topic: "Messaging & Real-time"
difficulty: Hard
problem: "WhatsApp"
---
# Design WhatsApp (Chat Messenger)

**Topic:** Messaging & Real-time · **Difficulty:** Hard · **Answer:** WhatsApp - Solution

## Prompt

Design a mobile chat application like WhatsApp. Users send text (and media) messages to one other person or to a group. Messages must arrive in near real time when the recipient is online and must be delivered reliably when they are offline or on a flaky network.

## Requirements to pin down (ask the interviewer)

- 1:1 only, or groups too? What is the max group size (assume 2-100 participants)?
- Media attachments? How long may the server keep a message for an offline user (assume ~30 days)?
- Multiple devices per user? Which message states are needed (sent, delivered, read)?
- Are calls, business accounts, registration, end-to-end encryption and spam prevention in scope? (Assume not.)

## Scale hints

- Billions of registered users; ~200M concurrent connections at peak
- ~40K messages/s sent (mostly 1:1), ~100K DB writes/s once per-recipient inbox entries are counted
- End-to-end delivery latency for online users: < 500 ms
- A message must never be lost once the sender sees "sent"; the server should keep messages no longer than needed

## Think about before opening the answer

1. What kind of connection does the client keep open, and what does that do to your server tier?
2. If sender and recipient are connected to different servers, how does the message find the right one?
3. What do you store, for how long, and what is the partition key? How does an offline user catch up?
4. How do you guarantee delivery (and avoid duplicates) when the recipient is offline, the pub/sub layer drops a message, or the network dies silently?
5. How does a message to a group (or to a user with several devices) differ from a 1:1 message?
6. How do you order messages in a conversation, and how would you show "last seen"?

## Self-check

- [ ] I can estimate concurrent connections and the number of chat servers
- [ ] I can explain how a message is routed across servers
- [ ] I can describe the ack protocol, heartbeats and the offline path
- [ ] I can explain group and multi-device fan-out and its cost
