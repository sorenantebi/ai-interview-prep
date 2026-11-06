---
difficulty: Hard
kind: multi-stage
---
# Friend recommendations at scale

**Kind:** Multi-stage (AI-enabled round) · **Difficulty:** Hard

## Scenario
The `friends` package powers the "People you may know" box of a small social network. Datasets are shipped as plain-text edge lists (one `a b` pair per line) and loaded into an in-memory graph. QA reports that after loading a dataset, friend lists look one-sided: some people show up in nobody's friend list. The recommendation feature itself was never finished, and product wants it to stay responsive on the production graph of about 10^5 users.

## Your tasks
1. **Fix the bug.** After loading an edge list, friendships are not visible from both sides. Find and fix the cause (the failing loader tests show the symptoms).
2. **Implement the feature.** `recommend_friends(graph, user, k)` in `friends/recommender.py` is a stub. It must return the top `k` people the user is not yet friends with, ranked by number of mutual friends (more first), ties broken by smaller user id. Details are in the function's docstring.
3. **Make it fast.** Hidden tests run recommendations on a graph with 10^5 users and several hundred thousand friendships (including a few very popular users) and assert a time budget. A solution that scans every user in the graph for every query will not pass.

## Notes
- Entry points: `FriendService` in `friends/service.py` is what the web layer calls; it delegates to `load_edges` and `recommend_friends`.
- `SocialGraph.friends_of` returns a safe copy of a user's friends; `SocialGraph.neighbors` returns the live set without copying. Treat the latter as read-only.
- Users are plain ints. Users with no friends may exist in the graph.
- Only the standard library is available.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
