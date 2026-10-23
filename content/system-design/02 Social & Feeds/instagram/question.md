---
topic: "Social & Feeds"
difficulty: Medium
problem: "Instagram"
---
# Design Instagram

**Topic:** Social & Feeds · **Difficulty:** Medium · **Answer:** Instagram - Solution

## Prompt

Design a photo and video sharing social network. Users upload photos or short videos with a caption, follow other users, and browse a feed of posts from the accounts they follow. Media must load quickly on slow mobile networks all over the world.

## Requirements to pin down (ask the interviewer)

- Photos only, or videos too? Maximum size and length of an upload?
- Is the feed chronological or ranked? Is an explore/discovery page in scope?
- Do we need likes and comments, stories, or direct messages? (usually: likes only, the rest out of scope)
- How long can a user wait between upload and the post being visible?
- Is the follow graph asymmetric? Are there accounts with tens of millions of followers?

## Scale hints

- ~500M DAU, ~100M new photos/videos per day
- Average photo ~2 MB original, short video ~20 MB
- Feed reads dominate uploads by more than 100x
- Media fetch latency must be low globally, upload must survive flaky connections

## Think about before opening the answer

1. How do you get big files from phones into storage without routing bytes through your API servers?
2. Where do thumbnails and different resolutions come from, and who produces them?
3. How is a post marked as visible only after its media is ready?
4. How do you serve billions of image requests per day cheaply and fast?
5. How is the feed assembled, and what is similar to or different from a text-only feed?
6. What do you store in the database and what goes in a blob store?

## Self-check

- [ ] I can estimate daily storage growth and CDN egress
- [ ] I can explain presigned URLs and resumable (multipart) uploads
- [ ] I can design an async media-processing pipeline with retries
- [ ] I can justify the feed approach (push, pull or hybrid) with numbers
