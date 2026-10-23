---
topic: "Storage & Caching"
difficulty: Medium
problem: "Dropbox"
---
# Design Dropbox (File Storage and Sync) – Solution

**Topic:** Storage & Caching · **Difficulty:** Medium · **Question:** Dropbox - Question

## 1. Requirements

**Functional**
- Upload a file from any device
- Download a file from any device
- Share a file with other users and view files shared with you
- Automatically sync files across a user's devices

**Non-functional**
- Availability over consistency: a device may briefly see stale state (eventual consistency), but must converge; one user's metadata commits still need atomic, versioned updates (no lost updates)
- Large files: up to ~50 GB, so uploads/downloads must be chunked and resumable
- Low latency for upload, download and sync; sync within a few seconds
- Security, reliability and recovery: encryption in transit and at rest, access control on every file, durable storage (11 nines target)
- Scale (our assumption): ~100M DAU, hundreds of millions of files, heavy-tailed file sizes

**Out of scope:** file editing/real-time collaboration, previews without downloading, designing the blob store itself, per-user quotas, full-text search, malware scanning as a core feature, version history (mention lightly: soft deletes and versions come cheaply from the commit log).

## 2. Back-of-envelope

- Storage: 500M users × ~1 GB ≈ **500 PB** raw. With dedup (often 20-30% savings) and cold tiering this is object-store territory, not database territory.
- Metadata: ~200 files per user × 500M = 100B file rows; at ~500 B each ≈ 50 TB. Chunk index adds more (one row per chunk). That is a **sharded relational DB**, not a single box.
- Chunk size ~8 MB (5-10 MB is typical; S3 multipart parts must be at least 5 MB): a 1 GB file is ~125 chunks, a 50 GB file ~6.4K chunks.
- Traffic: 100M DAU × ~2 file changes/day ≈ 200M uploads/day ≈ 2.3K/s avg, ~10K/s peak. Sync polling is the bigger load: 100M devices keeping a connection or polling every ~30 s ≈ 3M requests/s without push, which is why we use long-poll/WebSocket notifications.

## 3. Core entities and API

Core entities: **File** (the bytes, stored as chunks in blob storage), **FileMetadata** (name, size, MIME type, uploader, chunk list, version) and **User**. A separate **SharedFiles** mapping (`userId` partition key, `fileId` sort key) records shares, so we never embed a share list in the file record and "files shared with me" is one cheap query.

Our refinements for the deep dives:
- `FileMetadata { fileId, namespaceId, path, name, version, size, mimeType, uploaderId, chunkList[], modifiedAt, isDeleted }`
- `Chunk { hash (SHA-256), size, storageLocation, refCount }`  (global, content-addressed)
- `Namespace { namespaceId, ownerId, members[] }`  (a user root or a shared folder; the unit of sharding and ACLs)
- `Device { deviceId, userId, cursor }`

```
POST  /files/presigned-url        { name, size, mimeType, chunkHashes[] } -> { fileId, uploadId, presigned URLs for missing chunks }
PUT   <presigned S3 url>           (chunk bytes)                          -> 200 + ETag
PATCH /files/{fileId}/chunks      { chunkHash, etag, status }             -> chunk status updated (server verifies with S3)
POST  /files/{fileId}/commit      { uploadId, baseVersion }               -> { version }   (409 on conflict)
GET   /files/{fileId}/presigned-url                                       -> short-lived CDN-signed download URL
GET   /files/{fileId}                                                     -> file metadata (and download via the signed URL)
POST  /files/{fileId}/share       { userIds[], role }                     -> 200
GET   /files/changes?since=<cursor/timestamp>                             -> { entries[], newCursor }
```

## 4. High-level design

!Dropbox - Diagram.excalidraw

- **Metadata path:** clients talk to the File Service (stateless; generates presigned URLs and owns metadata) through the gateway. It owns files, versions, chunk lists and ACLs in a sharded Postgres/MySQL keyed by `namespaceId`.
- **Data path:** chunk bytes **never go through our API servers**. The client uploads straight to S3 with presigned URLs and downloads through a CDN. This keeps the API fleet small and cheap.
- **Download path:** the client asks for a download URL; the File Service checks the share/ACL and returns a short-lived **CDN-signed URL**; the CDN serves the bytes from the nearest edge and fetches from S3 on a miss.
- **Sync path:** local-change watchers on the client push uploads; a commit emits a change event to Kafka; the Notification Service wakes up other devices of the same namespace (WebSocket/long-poll), which then pull the delta from `/files/changes`. A periodic poll is the safety net for missed pushes (hybrid push + poll).
- **Async workers:** optional virus scan, thumbnails, garbage collection of unreferenced chunks.
- Start by getting this basic upload/download/share/sync flow working; the interesting depth is in large files, speed and security below.

## 5. Deep dives

### 5.1 Large files: chunked, resumable uploads (the main deep dive)

Why: a 50 GB file at 100 Mbps takes ~4,000 s (over an hour), well past request timeouts and gateway body limits (API gateways cap request bodies at a few MB), and any network blip loses everything.

| Approach | Verdict |
|---|---|
| Bad: single `POST` of the whole file | Hits timeouts/size limits, no progress, no resume |
| Good: client-side chunking (5-10 MB pieces) | Progress bar, retry per chunk, parallel upload. But the client reports chunk status, so a buggy or malicious client can claim chunks that never arrived |
| **Great: chunking + server-side verification** | Use the object store's multipart upload (`uploadId`, part numbers). The client sends each part's ETag; the server verifies against the store (S3 `ListParts`) before marking it uploaded, and calls `CompleteMultipartUpload` only when all parts are present. Chunk fingerprints (SHA-256) make resume trivial: after a crash, ask which fingerprints are done and continue |

Content-defined chunking (rolling hash) is the upgrade when edits insert bytes (see 5.2). The rest of this section (5.2 onward) covers how chunk hashes also drive dedup, sync and conflicts.

### 5.2 Chunking, hashing and deduplication

The client splits each file into chunks (fixed ~8 MB, or content-defined chunking with rolling hash) and computes a SHA-256 per chunk. The file is represented as an ordered list of chunk hashes.

| Approach | Pros | Cons |
|---|---|---|
| Whole-file upload | Trivial | Re-upload entire file after any edit, no resume |
| **Fixed-size chunks** | Simple, resumable, parallel upload, only changed chunks re-sent | An insert at the front shifts every later chunk, so all of them change |
| Content-defined chunking (Rabin/FastCDC) | Insertions only change local chunks; best dedup | More client CPU, variable chunk sizes, more complex |

Choose fixed ~8 MB for the interview and mention CDC as the upgrade for edit-heavy files. Because chunks are **content-addressed**, identical chunks across files (and across users) are stored once; `/files/init` returns only the hashes the server does not have. Cross-user dedup has a privacy leak (the "does this hash exist" oracle tells an attacker someone has a file), so many systems dedup only within an account or require proof of possession of the chunk.

### 5.3 Upload protocol, commit and atomic visibility

- `init` creates an `uploadId` and returns presigned URLs for missing chunks only (S3 multipart or one object per chunk).
- Chunks upload in parallel and independently; after a crash the client asks which chunks are done and continues.
- `commit` happens only when all chunks exist. The server verifies hashes, then atomically swaps the file's `chunkList` and increments `version` in one DB transaction. A file is never visible in a half-uploaded state.
- Orphaned chunks (never committed) are reclaimed by a GC job after N days.

!Dropbox - Deep Dive Diagram.excalidraw

### 5.4 Sync: how device B learns about changes

- Each namespace has a monotonically increasing **journal/change log** (`namespaceId, seq, fileId, op`). A device stores a `cursor` = last seq applied.
- Push-or-pull: the device holds a long-poll (or WebSocket) to the Notification Service; the server only says "something changed", and the client then calls `/changes?cursor=` to fetch entries. Tiny messages, and the metadata DB stays the source of truth.
- Polling alternative: simple but 100M devices × every 30 s is millions of QPS of mostly empty responses. Push-with-pull keeps cost proportional to actual changes.
- Notification fan-out: Kafka topic partitioned by `namespaceId`; Notification Service nodes subscribe to namespaces of their connected clients via a pub/sub (Redis) lookup.
- After a missed notification the cursor guarantees nothing is lost: the next poll or reconnect catches up.

### 5.5 Conflicts

Commit carries `baseVersion`. If the server's version differs, it returns 409 and the client keeps both: the loser is saved as `name (conflicted copy – device, date)`. This **last-writer-wins plus preserved copy** policy never destroys data. Merging (OT/CRDT) is only worth it for structured docs, which is out of scope.

### 5.6 Metadata storage and sharding

- Postgres/MySQL sharded by `namespaceId` (user root or shared folder), so a user's file tree is mostly one shard and commits are single-shard transactions.
- Shared folders are their own namespace, mounted into members' trees, so permission changes touch one place.
- Chunk index (`hash → location, refCount`) is a separate global key-value store (DynamoDB/Cassandra) sharded by hash; it is a pure lookup workload.
- Cache hot directory listings in Redis; invalidate on commit.

### 5.7 Speed: downloads, uploads, compression

- **Downloads:** CDN edge caching plus HTTP range requests for parallel and resumable downloads.
- **Uploads:** parallel chunk transfers to fill the pipe; adapt the chunk size to network conditions.
- **Sync:** send only the chunks that changed, not the whole file.
- **Compression:** compress before encrypting (ciphertext looks random and will not compress). Gzip is the safe default, Brotli compresses better, zstd is the fastest; decide per file type on the client (text compresses well, already-compressed media barely at all).

### 5.8 Security

- **In transit:** HTTPS everywhere. **At rest:** server-side encryption in the blob store with keys held separately.
- **Access control:** the SharedFiles/ACL data is checked by the File Service before it signs any URL.
- **Signed URLs:** upload/download URLs embed the path, an expiry (a few minutes, e.g. 5) and optionally an IP restriction; the CDN or S3 validates the signature. They are bearer tokens: anyone holding an unexpired URL can use it, so keep the lifetime short and never log them.

### 5.9 Cost, durability and failure modes

- S3 gives 11 nines with cross-AZ replication; add cross-region replication for disaster recovery. Tier cold chunks (not read for 90 days) to infrequent-access/Glacier classes.
- Deletes are soft (tombstone, kept for 30-180 days) and decrement `refCount`; GC deletes chunks at zero. A bug here destroys data, so run GC with a grace period and two-phase mark/sweep.
- Download hot spots (a shared viral file) are absorbed by the CDN with signed, expiring URLs; permissions are checked when issuing the URL, not at the CDN.
- Metadata shard down: failover to a synchronous replica; metadata is the crown jewel and uses sync replication within a region.
- Throttle per-user bandwidth and request rates; scan uploads asynchronously and block shared links on a positive verdict.

## 6. What interviewers look for

- **Mid-level (~80% breadth, 20% depth):** clear API and data model, a working upload/download/share design, presigned direct-to-S3 transfer, and an understanding of why chunking helps when asked.
- **Senior (~60/40):** finishes the baseline quickly and spends the time on large files: multipart upload mechanics, server-side verification, resumability; plus dedup with content addressing, CDC vs fixed chunks, push-with-pull sync, sharding by namespace, and clear trade-offs.
- **Staff+ (~40/60):** drives the depth unprompted and anticipates problems: GC safety and refcount races, cross-user dedup privacy, hot shared files, metadata shard failover, multi-region durability and cost tiering, conflict policy; treats the interviewer as a peer and steers the discussion.

## 7. Common pitfalls

- Streaming file bytes through application servers
- Re-uploading the whole file on small edits, or no resume support
- Polling every client constantly instead of notify-then-pull
- Treating sync as "last timestamp wins" and silently losing data
- Storing blobs in the relational database
- Forgetting garbage collection and chunk reference counts
