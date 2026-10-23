---
video: https://www.youtube.com/watch?v=IUrQ5_g3XKs
topic: "Storage & Caching"
difficulty: Medium
problem: "YouTube"
---
# Design YouTube (Video Upload and Streaming)

**Topic:** Storage & Caching · **Difficulty:** Medium · **Answer:** YouTube - Solution

## Prompt

Design a video sharing platform like YouTube. Creators upload videos, and viewers on phones, browsers and TVs, on fast or slow networks, watch them with minimal buffering. The service must handle the raw upload, convert it into formats every device can play, and deliver it globally.

## Requirements to pin down (ask the interviewer)

- Scope: upload and playback only? What about view counts, search, recommendations, comments, channels, live streaming?
- Maximum video length and size? Which resolutions do we support?
- How quickly after upload must a video be watchable?
- Do we need content moderation and copyright checks (usually out of scope)?

## Scale hints

- ~1M videos uploaded per day, ~100M videos watched per day
- Videos are large (tens of GB at the extreme; a 10 min 1080p source is often over 1 GB)
- Uploads must be resumable; availability is favoured over consistency
- Playback start time target: < 2 s, and no stalls even on poor bandwidth
- Heavy-tailed popularity: a tiny fraction of videos gets most views

## Think about before opening the answer

1. Why can't you just serve the uploaded file to viewers as it is?
2. How do you upload a multi-GB file reliably, and where do the bytes go?
3. How do you convert a video into many resolutions and formats fast, at huge scale?
4. How does adaptive bitrate streaming work, and what is stored?
5. How do you serve multiple Tbps of video egress economically (CDN, caching manifests and segments)?
6. How do you scale to 1M uploads/day and 100M views/day, and avoid hot partitions for viral videos?
7. (Optional extension) How do you count views without a hot-row problem?

## Self-check

- [ ] I can estimate upload storage and egress bandwidth
- [ ] I can explain segmenting, renditions and HLS/DASH manifests
- [ ] I can describe a parallel, retryable transcoding pipeline (DAG of segment tasks) and resumable multipart uploads
- [ ] I can explain CDN tiering for hot vs long-tail content
