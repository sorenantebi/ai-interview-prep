---
topic: "Social & Feeds"
difficulty: Medium
problem: "Instagram"
---
# Design Instagram – Solution

**Topic:** Social & Feeds · **Difficulty:** Medium · **Question:** Instagram - Question

## 1. Requirements

**Functional**
- Upload a photo or short video with a caption
- Follow / unfollow users
- View a feed of posts from followed accounts, with infinite scroll
- View a user's profile grid and a single post; like a post

**Non-functional**
- Fast media delivery worldwide (first image visible < 1 s on mobile)
- Uploads must be reliable on flaky networks (resumable)
- Durable media: never lose an acknowledged upload
- Feed freshness in seconds, availability over strict consistency

**Out of scope:** stories, DMs, explore ranking, ads, moderation models (mention hooks only).

## 2. Back-of-envelope

- Uploads: 100M/day ≈ **1.2K/s**, average ~5 MB (mix of photo and video) = **~500 TB/day of originals**. With 3 to 5 extra renditions, plan for ~1 PB/day raw growth, so media storage dominates all cost. Use S3 with lifecycle rules to move cold media to cheaper tiers.
- Feed reads: 500M × ~10 = 5B/day ≈ **58K/s average, ~200K/s peak**, mostly served from cache.
- Image views: ~20 images per feed load → 100B/day ≈ 1.2M/s. A **CDN must absorb >95%** of that, otherwise origin would drown.
- Metadata: ~500 B per post × 100M/day × 365 = **~18 TB/year**. Small. Metadata and media have completely different scaling profiles.

## 3. Core entities and API

Entities: `User`, `Follow`, `Post { postId, authorId, caption, mediaId, status, createdAt }`, `Media { mediaId, objectKey, type, renditions[], status }`, `Like { postId, userId }`.

```
POST /media/uploads        { type, sizeBytes }        -> { mediaId, uploadUrls[] }   (presigned)
POST /posts                { mediaId, caption }       -> { postId }
GET  /feed?cursor=&limit=                              -> { posts[], nextCursor }
GET  /users/{id}/posts?cursor=                         -> profile grid
```

Media bytes never pass through the API servers. The client uploads straight to blob storage with presigned URLs, then references the `mediaId` when creating the post.

## 4. High-level design

!Instagram - Diagram.excalidraw

- **Upload path:** client asks Post Service for upload URLs, uploads the original directly to S3, an object-created event starts media workers that produce renditions and mark the media `READY`.
- **Publish path:** once READY, a `post-created` event goes through Kafka (via an outbox/CDC off the metadata DB, so the DB write and event cannot diverge) to fan-out workers that push the post id into followers' feed lists.
- **Read path:** Feed Service reads ids from Redis, hydrates metadata, and returns CDN URLs. The client fetches pixels from the CDN, not from us.

## 5. Deep dives

### 5.1 Reliable uploads

| Approach | Pros | Cons |
|---|---|---|
| Upload through API servers | Simple, easy to validate | Ties up app servers on slow phone uploads, bandwidth cost, no resume |
| **Presigned URL straight to S3** | Offloads bytes, scales infinitely, multipart gives resume | Validate after the fact, need a completion signal |

Use **multipart upload** for large files (e.g. 5 MB chunks, upload in parallel, retry only failed parts). Presigned URLs expire in minutes and are scoped to one object key. The post row starts as `PENDING` and a post is invisible until its media is `READY`. An abandoned `PENDING` upload is cleaned by a TTL job and an S3 lifecycle rule for incomplete multipart uploads.

!Instagram - Deep Dive Diagram.excalidraw

### 5.2 Media processing pipeline

- S3 `ObjectCreated` event goes into a queue (SQS or Kafka). Workers (autoscaled on queue depth) generate: 1080, 640 and 150 px images (WebP/AVIF plus a JPEG fallback), blurhash placeholder, and for video an HLS/DASH ladder (e.g. 240p to 1080p) using ffmpeg.
- At-least-once delivery plus idempotent outputs (deterministic object keys) makes retries safe. Poison jobs go to a dead-letter queue.
- Videos are far more expensive than photos: separate queue and worker pool so video backlog never delays photos.
- Virus/CSAM/policy scanning runs as a stage before `READY`.

### 5.3 Serving media fast

- Put a CDN in front of S3 (CloudFront or similar). Object keys are immutable and content-addressed (`media/{hash}_{size}.webp`), so TTLs can be a year and invalidation is never needed.
- Clients ask for the right rendition by screen size and network. Origin shield (a mid-tier cache) cuts origin load further.
- Videos use adaptive bitrate streaming so the player switches quality as bandwidth changes.

### 5.4 Feed generation

Same core idea as FB News Feed - Solution: precompute per-user feed lists of post ids in Redis, hybrid fan-out (push for normal accounts, pull for accounts above a follower threshold). Difference here: every item is heavy media, so the feed response contains only metadata and **CDN URLs**, keeping responses small, and the client prefetches the next page's thumbnails. Ranked feeds score a ~500 post candidate set on read.

### 5.5 Data storage

| Data | Store | Reason |
|---|---|---|
| Media bytes | S3 (+ glacier tiers) | Cheap, durable (11 nines), CDN origin |
| Post / media metadata | Cassandra or sharded Postgres, key by `postId`; secondary table by `authorId, createdAt` for profile grid | Large, simple access patterns |
| Follow graph | Sharded SQL / KV, both directions | Fan-out needs followers, pull needs followees |
| Likes | Counter in Redis, durable rows in Cassandra, batched writes | Hot posts get huge write rates; avoid row-lock contention |
| Feeds | Redis | Latency |

### 5.6 Failure modes

- **Processing lag:** post stays PENDING; show the author a local preview so it feels instant.
- **Region loss:** replicate S3 cross-region, run active-active metadata, CDN keeps serving cached media.
- **Hot post (celebrity upload):** CDN absorbs views, like counters are sharded and flushed asynchronously.
- **Duplicate uploads:** client-generated idempotency key on `POST /posts`.

## 6. What interviewers look for

- **Junior:** separates metadata from blobs, uses a CDN, basic feed.
- **Mid:** presigned/multipart upload, async processing with a queue, renditions, caching, fan-out trade-off.
- **Senior:** outbox pattern, PENDING/READY state machine, cost math for storage and egress, ABR video, hot-key counters, failure and cleanup paths.

## 7. Common pitfalls

- Streaming uploads through the app tier
- Storing images in the relational database
- Making the post visible before processing finishes
- Serving full-resolution originals to every client
- Forgetting that the CDN, not your servers, handles most traffic
- Ignoring cleanup of orphaned multipart uploads and failed jobs
