---
topic: "Messaging & Real-time"
difficulty: Hard
problem: "WhatsApp"
---
# Design WhatsApp (Chat Messenger) – Solution

**Topic:** Messaging & Real-time · **Difficulty:** Hard · **Question:** WhatsApp - Question

## 1. Requirements

**Functional**
- Create chats (1:1 and groups of 2-100 participants) and send/receive messages in them
- Delivery states: sent, delivered, read
- Messages are kept for offline users and delivered when they reconnect (retention up to ~30 days)
- Media attachments (images, video, files)
- Multiple devices per user (extension)

**Non-functional**
- Low latency (< 500 ms) for online recipients
- **Deliverability:** at-least-once delivery with idempotent receive (effectively exactly-once for the user); never lose an acknowledged message
- Billions of users, ~200M concurrent connections, high throughput
- Minimal server-side storage: keep a message only until delivered (or a short retention window)
- Resilient to component failure; per-chat ordering; horizontally scalable

**Out of scope:** audio/video calls, business accounts, registration, exhaustive security (E2E encryption internals / Signal protocol), spam prevention.

## 2. Back-of-envelope

- ~200M concurrent connections. A tuned host can hold 1-2M sockets (WhatsApp's Erlang stack reportedly did); with a conservative ~100K per box (memory-bound, ~10-50 KB per socket) that is **~2K gateway servers**, with 1-2M per box a few hundred. Say which assumption you use.
- ~40K messages/s (mostly 1:1). Each message produces a message row plus one inbox entry per recipient client, so **~100K writes/s** at the DB. Message ~100 B text + ~100 B metadata.
- Storing everything forever is too much (hundreds of GB/day of text, growing into PBs per year). Hence "store until delivered, then delete" (or a 30-day cap) is a major cost lever; media goes to blob storage, never to the message store.
- Media: only a URL goes through chat; bytes go client to blob store (presigned URL) and are fetched via CDN.

## 3. Core entities and API

Entities: `User`, `Chat { chatId, participants }`, `Message { chatId, messageId, senderId, body | attachmentUrl, ts }`, `Client` (one per device of a user), plus an `Inbox` table (`clientId/userId, messageId`) holding messages not yet delivered.

All traffic uses one bidirectional WebSocket. Commands from the client:

```
createChat(participants[], name)          -> chatId
sendMessage(chatId, clientMsgId, body | attachmentUrl)   -> ack { serverMsgId, ts }
createAttachment(type, size)              -> { attachmentId, presignedUploadUrl }
modifyChatParticipants(chatId, userId, add | remove)
ack(serverMsgId, state: delivered | read)  (client -> server, for pushed events)
```

Events pushed by the server (each needs a client ack, else it is redelivered): `newMessage { chatId, serverMsgId, senderId, body }` and `chatUpdate { chatId, participants }`.

Plain HTTPS is used only for the presigned blob upload/download.

## 4. High-level design

!WhatsApp - Diagram.excalidraw

Single-host starting point: a chat server keeps an in-memory map `userId -> socket`, a DynamoDB-style store holds `Chat`, `Message` and `Inbox` tables, and attachments are uploaded straight to blob storage. Then scale it out:

1. The sender sends over its WebSocket to **Chat Server A**.
2. Chat Server A **writes the message and the recipients' inbox entries first**, then acks the sender ("sent"). Persist-before-ack is what guarantees no loss.
3. It **publishes** the message to the recipient's channel in **Redis Pub/Sub** (one channel per user). The chat server that holds the recipient's socket subscribed to that channel when the user connected.
4. **Chat Server B** receives it and writes it to the socket. The client acks ("delivered"), and the inbox entry is deleted.
5. If nobody is subscribed (offline), the entry stays in the inbox. The Push Service sends an APNs/FCM wake-up, and on reconnect the client drains its inbox.
6. Attachments: the client calls `createAttachment`, uploads to **blob storage** with the presigned URL, then sends the URL inside a normal message.

## 5. Deep dives

### 5.1 Scaling to billions: connection tier and cross-server routing

| Option | Verdict |
|---|---|
| One big host with an in-memory user map | Works for a demo; caps at 1-2M users, single point of failure |
| Sticky sharding of users to servers with a lookup table / session registry (Redis `userId -> serverId`, TTL refreshed by heartbeats) | Works: one lookup per message, but the registry is a hot dependency and can be stale |
| **Consistent-hash users to chat servers + Redis Pub/Sub with one channel per user** (**recommended**) | A server subscribes to `user:{id}` when the user connects; the sender's server just publishes. No registry to keep fresh, and Pub/Sub nodes are sharded with consistent hashing on the userId |
| Server-to-server calls | Every server must know every other; O(n^2) connections |

Chat servers are **stateful** (they hold sockets), so the load balancer is L4. Deploys must drain gracefully: tell clients to reconnect with jitter to avoid a thundering herd. Other protocols (MQTT, custom XMPP-like TCP as the real app uses) are worth a mention, but WebSocket is the pragmatic answer. Polling and long polling are rejected (waste, latency, battery); SSE is one-way only.

### 5.2 Storage and the inbox model

- Access pattern: "everything for user U after seq S", write-heavy, no joins. Use a wide-column/key-value store (**DynamoDB, Cassandra/ScyllaDB**): `Chat` keyed by `chatId`, `Message` by `chatId` + time-ordered `messageId`, `Inbox` by `userId` (or `clientId`) + `messageId`.
- A single relational DB would not sustain ~100K writes/s plus retention without sharding from day one.
- With "delete after delivery", inboxes stay small and hot; messages older than the 30-day cap are expired (TTL).

### 5.3 Delivery guarantees and acks

- Client generates `clientMsgId` and retries until it gets the server ack. The server de-duplicates on `(senderId, clientMsgId)`, so retries are safe.
- Server to recipient is also at-least-once: unacked events are redelivered; the client de-duplicates by `serverMsgId`.
- Ticks: server ack = one tick, device ack = two ticks, read receipt = blue ticks (receipts are small messages routed back to the sender).
- **Dead WebSockets (recommended: application-level heartbeats):** TCP can stay "open" long after a phone left coverage. Client and server exchange a heartbeat every ~10-30 s; the server drops the connection (and its Pub/Sub subscription) when acks time out, so failures are detected in seconds, and the message falls to the offline path.
- **Pub/Sub is fire-and-forget:** a publish can be lost (subscriber reconnecting, node failover). Therefore **write to the inbox before publishing**, and on every (re)connect sync from durable storage. Optional extras: periodic polling of the inbox, and per-chat sequence numbers so the client detects gaps and asks for the missing range.

### 5.4 Ordering

- Simple option: the server stamps each message with a timestamp (clocks synced via NTP) and clients display in receive order. Good enough for chat because small skew is invisible.
- Stricter option: server-assigned monotonic sequence **per chat**, which also enables gap detection. A global order is never needed.
- The sender may show optimistic local order until the ack arrives.

### 5.5 Group chats and multiple devices

!WhatsApp - Deep Dive Diagram.excalidraw

- A group message is stored **once** and fanned out as one inbox entry per recipient client, plus one Pub/Sub publish per recipient user. With groups capped at 100, the chat server can do this itself (members are cached); no extra queue needed.
- Multiple devices: track each device as a `Client`; the inbox is per client, and a message is replicated to every active client of each participant. Each client acks and drains independently.
- Larger groups (1,000+) or broadcast lists: move fan-out to a queue (Kafka partitioned by `chatId`) with a worker pool, or fan out on read from a shared log.

### 5.6 Presence ("last seen") and typing

- Do **not** write to the DB on every heartbeat. Store `lastSeen` only when a user disconnects.
- "Is the user online now?" is answered from the live state (is anyone subscribed to the user's channel / connection map); otherwise return the stored disconnect time.
- Typing indicators are ephemeral, never persisted; only subscribe for the open chat to avoid O(contacts) amplification.

### 5.7 Failure modes

- **Chat server crash:** clients reconnect (jittered backoff) to any server and resubscribe; undelivered inbox rows are replayed on connect.
- **Pub/Sub node failure:** subscriptions are re-established on failover; messages published in the gap are recovered by the inbox sync (see 5.3).
- **Hot group:** rate limit senders; cap size.
- **Multi-region:** users homed to the nearest region, cross-region delivery via inter-region queue; the inbox stays in the recipient's home region. At Staff+ level, discuss cell-based architecture so one failure only hits a slice of users.

## 6. What interviewers look for

- **Mid-level:** define the WebSocket API, build a working design (chat server, DB, inbox for offline users, blob storage for attachments), propose a rough way to scale and acknowledge the gaps.
- **Senior:** go deep on 2-3 topics: cross-server routing with consistent hashing and Pub/Sub, persist-before-ack and idempotency keys, heartbeats, multi-device inboxes, capacity math, graceful drain and reconnect storms, trade-offs between options.
- **Staff+:** go two or three levels down on failure modes and bottlenecks (Pub/Sub loss, hot channels, reconnect storms), regionalization and cell-based architecture, retention/cost reasoning, and bring patterns from real systems.

## 7. Common pitfalls

- Using HTTP polling or a stateless REST API for message delivery
- Acking the sender before the message is durably stored
- Forgetting how the second server finds the recipient's connection
- Treating Pub/Sub as durable (no inbox write before publish)
- Writing `lastSeen` to the DB on every heartbeat
- Storing media bytes in the message DB
- Promising a global total order instead of per-chat order
- Ignoring reconnect storms, dead connections and the offline path
