---
topic: "Messaging & Real-time"
difficulty: Hard
problem: "Google Docs"
---
# Design Google Docs (Collaborative Document Editing) – Solution

**Topic:** Messaging & Real-time · **Difficulty:** Hard · **Question:** Google Docs - Question

## 1. Requirements

**Functional**
- Create, open and edit documents; multiple users edit the same document concurrently
- Collaborators see each other's edits and cursors in near real time
- All clients converge to the same document state
- Sharing with permissions; version history (as an extension)

**Non-functional**
- Low latency: local edits apply instantly, remote edits visible in < 200 ms
- **Strong convergence** (every replica ends identical) and no lost edits
- Durable: an acknowledged edit is never lost
- Scalable to ~1B documents; availability matters, but consistency inside one document matters more

**Out of scope:** rich-text schema details, spreadsheets/slides, comments and suggestions, full-text search.

## 2. Back-of-envelope

- 100M DAU × ~1 hour editing, one op per ~0.5 s of typing → on average **~100K-1M ops/s** system-wide (batch keystrokes into ~100-300 ms ops).
- Op ≈ 50-100 B. 1M ops/s × 100 B = 100 MB/s ≈ **8 TB/day** of op log (before compaction).
- Concurrent open documents maybe ~20M, mostly with a single editor. One collaboration server can own ~50K active documents, so a few hundred servers.
- A document's text is ~100 KB on average; snapshots total ~100+ TB for 1B documents, so it belongs in blob storage.

## 3. Core entities and API

Entities: `Document { docId, ownerId, title, headRev }`, `Operation { docId, rev, authorId, ops, ts }`, `Snapshot { docId, rev, content }`, `ACL { docId, principal, role }`.

```
POST /docs                         -> create, returns docId
GET  /docs/{id}                    -> latest snapshot + ops since snapshot (initial load)
WS   /docs/{id}/session            -> bidirectional realtime channel
  -> { type: "op", baseRev, ops }          client edit (based on server revision it has seen)
  <- { type: "ack", rev }                   server accepted
  <- { type: "op", rev, authorId, ops }     remote edit, already transformed
  <-> { type: "cursor", userId, pos }       ephemeral presence
```

## 4. High-level design

!Google Docs - Diagram.excalidraw

- Clients keep a WebSocket to a gateway, which authenticates (ACL check against Postgres) and routes the session to the **Collab Service instance that owns the document**, found via a `docId → server` map in Redis (or consistent hashing on `docId`).
- That instance is the **single writer** for the document: it orders operations, transforms them, appends to the op log and broadcasts to all connected editors.
- Ops are persisted to an append-only log; a background worker periodically writes a **snapshot** to blob storage so loads do not replay the full history.
- Cursor/presence updates are broadcast but never persisted.

## 5. Deep dives

### 5.1 Concurrency control: OT vs CRDT (and what not to do)

| Approach | How it works | Pros | Cons |
|---|---|---|---|
| Locking (per paragraph/doc) | Take a lock before editing | Simple | Terrible UX, deadlocks, not real-time |
| Last-write-wins on the document | Whole-doc overwrite | Trivial | Silently destroys concurrent edits. Reject |
| **Operational Transformation (OT)** | Central server orders ops; ops based on stale revisions are *transformed* against ops they missed | Compact ops, proven (Google Docs), simple clients | Transform functions are tricky to get right; needs a central sequencer |
| **CRDT** (e.g. RGA, Yjs, Automerge) | Each character gets a unique, ordered id; ops commute | No central server needed, great for offline and P2P | Metadata overhead (ids/tombstones), history can grow, more memory |

Example: doc "AB", rev 5. User 1 inserts "X" at index 1 (→ "AXB"); user 2 concurrently inserts "Y" at index 1. The server accepts user 1's op as rev 6. User 2's op, based on rev 5, is transformed against rev 6: because an insert at the same index tie-breaks by a deterministic rule (e.g. author id), it becomes "insert Y at index 2". Server applies as rev 7, broadcasts it, and everyone ends with "AXYB". Clients run the symmetric transform on their *pending local* ops against incoming ones.

Pragmatic answer: **OT with a central server** when a server is already in the loop (this problem). Mention CRDTs as the right choice for offline-first/P2P.

### 5.2 The OT flow and the single-writer server

!Google Docs - Deep Dive Diagram.excalidraw

- Client protocol: send at most **one op in flight** (the rest are buffered and composed). This keeps the client's state machine simple: states "synchronized", "awaiting ack", "awaiting ack with buffer".
- Server: for an incoming op with `baseRev = r` and head `h`, transform it against ops `r+1..h`, apply, assign `rev = h+1`, append to log, ack the sender, broadcast the transformed op to others.
- Because ops for one document pass through **one serial queue**, the order is total and no distributed consensus is needed on the hot path. All the difficulty is routing a document to exactly one owner.

### 5.3 Routing, ownership and failover

- `docId → owner` via consistent hashing, or a lease in Redis/etcd/ZooKeeper (`SET docId owner NX PX 30000`, renewed by heartbeat).
- **Owner crash:** clients reconnect, the gateway resolves a new owner, which rebuilds state = latest snapshot + replay of ops since (read from the log). Clients resend un-acked ops with their client-generated op id; the server de-duplicates by `(clientId, clientSeq)`.
- Fencing: attach a lease epoch to every log append so a zombie old owner (GC pause, network partition) cannot write. The log enforces `rev` uniqueness (conditional insert) as the final guard.
- Idle documents are evicted from memory after a few minutes; the next open reloads them.

### 5.4 Storage: op log plus snapshots

- **Op log:** `(docId, rev) → op`, append-only. Cassandra/DynamoDB/Spanner-style KV works; Postgres is fine at smaller scale. Partition by `docId`.
- **Snapshots:** every ~1,000 ops or N minutes, a worker materialises text at rev R and stores it in S3 (key `docId/R`). Loading = latest snapshot + tail of the log (a few hundred ops at most).
- **Version history:** free, because the log is complete; named versions point to a rev. Compaction may fold old ops into snapshots after a retention window.
- **Metadata/ACL:** Postgres (relational: sharing, folders, ownership), cached.

### 5.5 Presence, cursors, scale limits

- Cursor positions are ephemeral, rate-limited (~10/s) and transformed with ops so they stay anchored to text. Pub/sub within the owning server; no durable storage.
- Fan-out per edit is O(editors); with 100 editors it is fine. For huge audiences (view-only 10K+), serve readers from a read-only replica stream with coarser batching.
- Large documents: chunk the snapshot and paginate the editor viewport; cap op size and rate per user.

### 5.6 Offline and failure modes

- **Offline editing:** client buffers ops locally (IndexedDB) and on reconnect sends them with the old `baseRev`; the server transforms across the gap. For long offline sessions, CRDT-style merging (or a prompt to the user) handles large divergence better.
- **Network blips:** ops are idempotent by client seq; the reconnect handshake carries `lastKnownRev` so the server sends only missing ops.
- **Corrupt transform bug:** keep periodic checksum/hash of the document in acks; a mismatch makes a client reload from the server's snapshot.

## 6. What interviewers look for

- **Junior:** WebSocket for real-time, store documents in a DB, mentions conflict problem.
- **Mid:** OT or CRDT named and explained with an example, op-based sync rather than whole-document sync, snapshots plus log.
- **Senior:** single-writer per document with leases and fencing, client state machine (one op in flight), failover replay and idempotency, OT-vs-CRDT trade-offs, compaction and history, presence handled separately from durable state.

## 7. Common pitfalls

- Locking or last-write-wins
- Sending the entire document on each change
- Applying remote ops without transforming against pending local ops
- Letting any server handle any document, leaving the order undefined
- No snapshots, so loading replays the whole history
- Persisting cursor positions
