---
video: https://www.youtube.com/watch?v=l38XL9914fs
topic: "Search & Analytics"
difficulty: Hard
problem: "FB Post Search"
---
# Design Facebook Post Search

**Topic:** Search & Analytics · **Difficulty:** Hard · **Answer:** FB Post Search - Solution

## Prompt

Design a search feature for a large social network. Users type a keyword query (e.g. "pasta recipe") and get back a ranked list of posts that match. Users create and like posts at a high rate, and a new post should become searchable quickly.

## Requirements to pin down (ask the interviewer)

- Which posts can a searcher see: public only, or also friends-only posts? (This changes the whole design.)
- Do we need typeahead / autocomplete, or only full-query search?
- Sort order: by recency, by like count, or personalised relevance? Are likes in scope as a write path?
- How fresh must results be: seconds, or minutes?
- Do edits and deletions have to be reflected in search?
- Are multiple languages and hashtags in scope?

## Scale hints

- ~1B users, ~1 post/day each (~10K posts/s) and ~10 likes/day each (~100K likes/s): the system is write-heavy
- Search traffic ~10K queries per second
- Search latency target: median < 500 ms; new posts searchable within a minute
- The corpus keeps growing (order of PBs over 10 years), all posts must stay discoverable, but most queries want recent content

## Think about before opening the answer

1. What data structure makes keyword search fast, and why does a SQL `LIKE '%word%'` not work?
2. How do you split the index across machines, and what does a query look like when the index is sharded?
3. How do you keep the index fresh without rewriting the whole thing for every new post?
4. Where does ranking happen, and how do you avoid scoring millions of candidates?
5. How do you handle 100K likes/s when results can be sorted by like count, and how do you search for multi-word phrases?
6. How do you keep the index small and cheap given that most posts are rarely searched, and how do you serve 10K QPS of repetitive queries (caching)?
7. (Extension) How do you make sure a user never sees a post they are not allowed to see?

## Self-check

- [ ] I can explain an inverted index with posting lists and how AND queries are evaluated
- [ ] I can design the write path (post -> queue -> indexer) and justify its freshness trade-offs
- [ ] I can describe scatter-gather, top-K merging and tail latency
- [ ] I can handle high like volume (milestone updates + re-ranking) and phrase queries (bigrams)
- [ ] I can propose a tiered index (recent/hot vs. archive) and a privacy filtering strategy
