---
topic: "Heap / Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/design-twitter/
neetcode: https://neetcode.io/problems/design-twitter-feed
---
# Design Twitter - Solution

**Question:** Design Twitter - Question · **Difficulty:** Medium

## Intuition

Each user's tweets are already in chronological order in their own list, so building a feed is a **merge of k sorted lists** where we only need the first 10 items. A max-heap seeded with the newest tweet from each relevant user lets us pull the global newest, then advance into that user's list — just like merging k sorted lists.

## Approach

1. Keep a global counter `time` that increases on every post, `tweets[user] = [(time, tweetId), ...]`, and `following[user] = set()`.
2. `postTweet`: append `(time, tweetId)` and increment `time`.
3. `follow` / `unfollow`: add to / discard from the follower's set (ignore self-follow).
4. `getNewsFeed`: for the user and each followee with tweets, push `(-time, tweetId, user, index)` of their latest tweet.
5. Pop up to 10 times; after each pop, push the same user's previous tweet (`index - 1`) if it exists.

## Code

```python
class Twitter:
    def __init__(self):
        self.count = 0
        self.tweetMap = defaultdict(list)  # userId -> list of [count, tweetIds]
        self.followMap = defaultdict(set)  # userId -> set of followeeId

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweetMap[userId].append([self.count, tweetId])
        self.count -= 1

    def getNewsFeed(self, userId: int) -> List[int]:
        res = []
        minHeap = []

        self.followMap[userId].add(userId)
        for followeeId in self.followMap[userId]:
            if followeeId in self.tweetMap:
                index = len(self.tweetMap[followeeId]) - 1
                count, tweetId = self.tweetMap[followeeId][index]
                heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])

        while minHeap and len(res) < 10:
            count, tweetId, followeeId, index = heapq.heappop(minHeap)
            res.append(tweetId)
            if index >= 0:
                count, tweetId = self.tweetMap[followeeId][index]
                heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])
        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followMap[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.followMap[followerId]:
            self.followMap[followerId].remove(followeeId)
```

## Complexity

- **Time:** `postTweet`, `follow`, `unfollow` are `O(1)`; `getNewsFeed` is `O(F + 10 log F)` where `F` is the number of followees (heapify plus at most 10 pops/pushes).
- **Space:** `O(U + T + E)` for users, tweets, and follow edges; the feed heap uses `O(F)`.

## Other Approaches

- **Collect and sort:** gather all tweets of the user and followees, sort by time, take 10 — Time `O(N log N)` per feed where `N` is the total relevant tweets, Space `O(N)`.
- **Cap stored tweets:** only keep each user's last 10 tweets (enough for any feed), bounding memory per user — same heap merge, Space `O(10 * U)` for tweets.

## Key Takeaway

A news feed is "merge k sorted lists, take the top 10": seed a heap with each source's newest item and lazily advance only the source you popped from.
