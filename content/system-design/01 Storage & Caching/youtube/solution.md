---
topic: "Storage & Caching"
difficulty: Medium
problem: "YouTube"
---
# Design YouTube (Video Upload and Streaming) – Solution

**Topic:** Storage & Caching · **Difficulty:** Medium · **Question:** YouTube - Question

## 1. Requirements

**Functional**
- Users can upload videos
- Users can watch (stream) videos

**Non-functional**
- High availability, favouring availability over consistency
- Support very large videos (tens of GB) with **resumable uploads**
- Low-latency streaming, even on poor bandwidth (adaptive quality, playback start < 2 s)
- Scale: ~1M videos uploaded/day, ~100M videos watched/day
- Processed video available within minutes of upload (our addition)

**Out of scope:** view counts, search, recommendations, comments, channels/subscriptions, content moderation, bot prevention, monitoring/alerting, live streaming, ads, DRM (mention as extensions). View counting is kept as a short optional discussion in 5.5.

## 2. Back-of-envelope

- Uploads: 1M videos/day ≈ 12/s average. With sources of tens of GB at the extreme but ~1 GB typical, that is ~1 PB/day raw. Transcoded renditions (a ladder of 6-8 resolutions) add roughly another 1-2x, so plan for **~2-3 PB/day**, around 1 EB/year. Object storage with tiering, not a database.
- Egress: 100M views/day × ~200 MB per view (~10 min at ~2.5 Mbps) ≈ 20 PB/day ≈ **~2 Tbps** average, several Tbps at peak. No origin can serve this, so **a CDN is mandatory** and cache hit ratio is the dominant cost lever.
- Metadata is small: 1M/day ≈ 365M records/year × ~2 KB ≈ 0.7 TB/year. Easy to partition by `videoId`.
- Transfer time: a 10 GB video on a 100 Mbps link takes 13+ minutes in one piece, which is why uploads are chunked and playback is segmented.
- Transcoding compute: tens of thousands of video hours per day need a large worker fleet, which is why work is split into parallel segment tasks and scaled on queue depth.
- (If an interviewer instead uses real-world YouTube numbers, ~500 h uploaded/min and ~1B h watched/day, the same design holds but egress is ~80 Tbps and own-ISP cache appliances become relevant.)

## 3. Core entities and API

Core entities: **User** (uploader or viewer), **Video** (the bytes: raw upload plus processed segments), **VideoMetadata** (title, description, uploader, status, chunk upload status, manifest and segment URLs). Optional extras: `Rendition { videoId, resolution, codec, bitrate }`, `ViewCount { videoId, count }`.

`VideoMetadata { videoId, ownerId, title, description, status (UPLOADING/PROCESSING/READY/FAILED), chunks[{fingerprint, status}], manifestUrl, createdAt, duration }`

```
POST  /presigned_url        { title, description, size, chunkFingerprints[] } -> { videoId, uploadId, presigned multipart URLs }
PATCH /videos/{id}/chunks   { fingerprint, etag, status: Uploaded }           -> chunk status updated (server verifies the ETag)
GET   /videos/{id}                                                           -> VideoMetadata incl. manifest URL
GET   <cdn>/{id}/master.m3u8, /{id}/720p/seg_0042.ts                          (HLS; DASH is analogous)
```
There is no explicit "complete" call: the object store emits an event when the multipart upload finishes, which starts processing.

## 4. High-level design

!YouTube - Diagram.excalidraw

- **Upload path:** the client asks the **Video Service** for presigned URLs, then uploads the raw file straight to object storage (S3 multipart, resumable). The completed upload emits an event to the processing orchestrator.
- **Processing path:** the orchestrator runs a DAG of tasks on a worker fleet: split into segments, transcode each into several formats/resolutions, produce audio/transcripts, write manifests into the processed store, then flip `status = READY` and record segment URLs in the metadata DB.
- **Watch path:** the player fetches `VideoMetadata`, then the manifest (the index of available segments per rendition), then downloads segments adaptively based on measured bandwidth, from the CDN. Only on a CDN miss does a request reach the origin (processed S3).
- Metadata is a small, read-heavy dataset partitioned by `videoId`: Cassandra (leaderless, consistent hashing) or sharded MySQL/Postgres, with an LRU **metadata cache** in front for hot videos.

## 5. Deep dives

### 5.1 Why transcode and what is "adaptive streaming"?

Source uploads come in arbitrary codecs, sizes and bitrates and are far too large for mobile networks. We convert each video into a **ladder of renditions** (e.g. 144p to 4K, H.264 everywhere, plus VP9/AV1 for popular videos where lower bitrate repays the extra encode cost) and cut each rendition into 2-10 s **segments**. A text **manifest** (HLS `.m3u8` or DASH `.mpd`) lists segments per rendition. The player measures throughput and buffer level and switches rendition between segments (ABR). Files are plain HTTP objects, so any CDN and any browser works; no special streaming server is needed.

| Option | Pros | Cons |
|---|---|---|
| Serve the original file | No processing | Wrong codec/size, no ABR, huge egress |
| One rendition per video | Cheap | Stalls on slow links, wasteful on fast ones |
| **Segmented multi-rendition (HLS/DASH)** | ABR, cacheable segments, fast seek, parallel encode | More storage, a processing pipeline |

### 5.2 Resumable large uploads

- The client splits the video into chunks of ~5-10 MB (S3 multipart parts must be at least 5 MB), fingerprints each, and registers the chunk list with status `NotUploaded` via the Video Service. Parts upload in parallel to presigned URLs; after each, the client reports the ETag with `PATCH /videos/{id}/chunks` and the server checks it against the fingerprint/S3 before marking the chunk `Uploaded`.
- To resume (even days later, using the `uploadId`), the client fetches the metadata and uploads only the chunks that are not `Uploaded`. S3 emits one object-level event when the multipart upload completes, and that event starts processing.
- Bytes never pass through app servers.
- Validate container/codec early, enforce size and duration limits, and run a malware check.
- Expire abandoned multipart uploads with a bucket lifecycle rule.

### 5.3 The transcoding pipeline (DAG of tasks)

!YouTube - Deep Dive Diagram.excalidraw

- A **splitter** cuts the source at keyframe (GOP) boundaries into chunks, so each chunk can be encoded independently.
- A scheduler turns that into a DAG: per-segment × per-rendition encode tasks run in parallel on a worker fleet (spot/preemptible instances are fine because tasks are idempotent and retried), then a **packager** merges and writes manifests. Thumbnails, audio tracks, captions and moderation run beside the video encode.
- Queue: Kafka or SQS plus a workflow engine (e.g. Temporal/Airflow style) to track task state, retries with backoff and dead-letter handling. Tasks write to deterministic object keys, so retries are safe.
- Priority: publish a **low-resolution rendition first** so the video is watchable within minutes; higher resolutions arrive later. Popular creators or trending content get priority queues.
- Failure modes: poison input (corrupt file) goes to the DLQ and sets `FAILED`; a worker dying mid-task just re-runs that segment; use heartbeats/visibility timeouts.

### 5.4 Serving multi-Tbps egress: CDN and caching

- Segments are immutable, so they have `Cache-Control` of days or longer: ideal CDN content.
- Tiered caching: **edge PoP** (most traffic) → **regional/shield cache** → origin S3. Shielding collapses concurrent misses into one origin fetch.
- Popularity is a power law: pre-warm or push new videos from big creators to edges; for the long tail, serve from regional caches with a lower hit rate, and keep the processed copy in a cheaper storage class.
- Large players run their own cache appliances inside ISP networks (an Open Connect style approach) to cut transit cost; a smaller design uses commercial CDNs, multi-CDN for resilience.
- Signed URLs/tokens protect private or unlisted videos; the manifest endpoint enforces visibility.

### 5.5 Metadata and view counts

- Metadata: read-heavy, cacheable, sharded by `videoId`. A video's detail page is served from Redis/CDN with short TTLs.
- View counting: one DB row incremented per view creates a **hot key** on viral videos. Instead, players/CDN logs emit view events to Kafka; a stream processor (Flink/Spark) aggregates per video per minute and writes batched increments to a counter store (Redis/Cassandra counters, periodically flushed to the DB). Displayed counts are eventually consistent, and fraud filtering (bots, repeat views) happens in the stream job.

### 5.6 Scaling to 1M uploads and 100M views a day

- **Video Service:** stateless, horizontally scaled behind the load balancer.
- **Metadata store:** Cassandra partitioned by `videoId` spreads load evenly; the caveat is hot partitions for viral videos, handled with the LRU cache (partitioned by `videoId`) and extra replicas for hot rows.
- **Processing:** the worker fleet autoscales on job-queue depth; segments run in parallel on different nodes.
- **Storage:** S3 scales by itself (cross-AZ replication in-region); global viewers need the CDN for geographic reach. The CDN caches both manifests and segments.

### 5.7 Storage tiers and failures

- Keep the raw original (for re-encoding with newer codecs) in cold storage; keep only the popular renditions in the hot tier. Re-encode on demand for old videos when a rendition is missing.
- Multi-AZ durability from S3. CDN failure: fail over to a second CDN. Origin overload: shield + request coalescing; rate limit uploads per user.

## 6. What interviewers look for

- **Mid-level (~80% breadth, 20% depth):** clear API and data model, a working upload and playback design, converges on multipart upload plus segment-based streaming, understands the direct-to-S3 interface, and goes deep on one topic.
- **Senior (~60/40):** quick high-level design, then extensive depth on video post-processing (parallel segment-level DAG with idempotent retries, ABR mechanics) and upload mechanics (multipart, chunk verification); articulates trade-offs such as CDN tiers/cost, codec and storage-tier choices.
- **Staff+ (~40/60):** brings hands-on depth and anticipates problems unprompted: hot partitions and viral videos, CDN strategy and failover, queue/worker autoscaling and cost, priority and failure handling in the pipeline, multi-region; treats the interviewer as a peer and may steer to the most interesting area.

## 7. Common pitfalls

- Streaming uploads through application servers
- Serving the raw file, or a single resolution
- Running transcoding synchronously in the upload request
- One monolithic encode job per video (slow, restarts from zero on failure)
- Incrementing a single DB row per view
- Ignoring egress cost and the CDN hit ratio
