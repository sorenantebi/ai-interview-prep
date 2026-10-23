---
topic: "Heap / Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/design-twitter/
neetcode: https://neetcode.io/problems/design-twitter-feed
---
# Design Twitter

**Topic:** Heap / Priority Queue · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/design-twitter/) · [NeetCode](https://neetcode.io/problems/design-twitter-feed)

## Problem

Design a tiny social feed service. Users can post tweets, follow and unfollow other users, and fetch a news feed containing the **10 most recent** tweet IDs posted by themselves or by anyone they follow, ordered from newest to oldest.

Implement `Twitter`:

- `Twitter()` creates an empty service.
- `void postTweet(int userId, int tweetId)` records a new tweet with a unique `tweetId` by `userId`. Each call is more recent than all previous calls.
- `List[int] getNewsFeed(int userId)` returns up to 10 tweet IDs from the user and their followees, most recent first.
- `void follow(int followerId, int followeeId)` makes `followerId` follow `followeeId`.
- `void unfollow(int followerId, int followeeId)` makes `followerId` stop following `followeeId` (no-op if not following).

A user always sees their own tweets; following or unfollowing oneself has no effect on that.

## Examples

**Example 1**
```text
Input:  ["Twitter","postTweet","getNewsFeed","follow","postTweet","getNewsFeed","unfollow","getNewsFeed"]
        [[],[1,5],[1],[1,2],[2,6],[1],[1,2],[1]]
Output: [null,null,[5],null,null,[6,5],null,[5]]
```

**Example 2**
```text
Input:  ["Twitter","postTweet","postTweet","getNewsFeed"]
        [[],[1,1],[1,2],[2]]
Output: [null,null,null,[]]
Explanation: user 2 follows nobody and has no tweets
```

## Constraints

- `1 <= userId, followerId, followeeId <= 500`
- `0 <= tweetId <= 10^4`, all tweet IDs are unique
- At most `3 * 10^4` total calls
