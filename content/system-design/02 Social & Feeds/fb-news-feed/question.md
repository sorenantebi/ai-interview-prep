---
video: https://www.youtube.com/watch?v=Qj4-GruzyDU
topic: "Social & Feeds"
difficulty: Medium
problem: "FB News Feed"
---
# Design Facebook News Feed

**Topic:** Social & Feeds · **Difficulty:** Medium · **Answer:** FB News Feed - Solution

## Prompt

Design the news feed of a large social network. Users create posts (text, photos, links) and follow/friend other users. When a user opens the app they see a feed of recent posts from the people they follow, newest or most relevant first, and can scroll through it endlessly.

## Requirements to pin down (ask the interviewer)

- Is the feed chronological (newest first) or ranked? How sophisticated is the ranking in scope?
- Is the relationship symmetric (friends) or asymmetric (follow)? Is there any cap on how many accounts a user can follow, and are there accounts with millions of followers?
- Which post types do we support, and who handles media storage and delivery?
- How fresh must the feed be? Do we favour availability over consistency, and is up to a minute of delay acceptable?
- Do we need likes/comments or visibility rules, or only the posts themselves?

## Scale hints

- ~2B total users, ~500M daily active, each opening the feed ~10 times a day
- ~200M new posts per day, average user follows a few hundred accounts
- A few accounts have 10M+ followers, and users may follow thousands of accounts
- Post creation and feed load latency target: < 500 ms end to end; a new post visible to followers within about a minute

## Think about before opening the answer

1. What are the core entities and the two or three APIs you need?
2. Do you assemble the feed when it is read, or precompute it when a post is written? What does each choice cost?
3. What breaks when one author has 10 million followers?
4. How do you paginate an endless feed that keeps receiving new items?
5. Where do you cache, and what exactly do you store in the cache?
6. What happens when one post is suddenly read by millions of feeds at once?
7. How do you keep the system serving feeds when a cache or a datastore fails?

## Self-check

- [ ] I can estimate feed read QPS and the write amplification of fan-out
- [ ] I can compare fan-out on read, fan-out on write and a hybrid
- [ ] I can design cursor-based pagination and explain why offsets fail
- [ ] I can describe how ranking plugs into the pipeline without slowing reads
