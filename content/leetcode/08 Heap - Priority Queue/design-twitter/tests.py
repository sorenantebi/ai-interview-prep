import sys
import heapq
from collections import defaultdict, deque
from typing import List, Optional, Dict


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_list(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict,
      "defaultdict": defaultdict, "heapq": heapq, "deque": deque}
exec(open("attempt.py").read(), ns)


def run_ops(ops, args):
    Twitter = ns["Twitter"]
    obj = None
    results = []
    for op, a in zip(ops, args):
        if op == "Twitter":
            obj = Twitter()
            results.append(None)
        else:
            r = getattr(obj, op)(*a)
            results.append(r if op == "getNewsFeed" else None)
    return results


def brute_force(ops, args):
    tweets = []
    follows = defaultdict(set)
    results = []
    for op, a in zip(ops, args):
        if op == "Twitter":
            results.append(None)
        elif op == "postTweet":
            tweets.append((a[0], a[1]))
            results.append(None)
        elif op == "getNewsFeed":
            u = a[0]
            vis = follows[u] | {u}
            feed = [t for (usr, t) in reversed(tweets) if usr in vis][:10]
            results.append(feed)
        elif op == "follow":
            if a[0] != a[1]:
                follows[a[0]].add(a[1])
            results.append(None)
        elif op == "unfollow":
            follows[a[0]].discard(a[1])
            results.append(None)
    return results


cases = []

# Example 1
cases.append((
    ["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"],
    [[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]],
    [None, None, [5], None, None, [6, 5], None, [5]],
))

# Example 2
cases.append((
    ["Twitter", "postTweet", "postTweet", "getNewsFeed"],
    [[], [1, 1], [1, 2], [2]],
    [None, None, None, []],
))

# Empty feed for brand new user
cases.append((
    ["Twitter", "getNewsFeed"],
    [[], [1]],
    [None, []],
))

# More than 10 tweets, only latest 10
ops = ["Twitter"] + ["postTweet"] * 15 + ["getNewsFeed"]
args = [[]] + [[1, i] for i in range(15)] + [[1]]
cases.append((ops, args, None))

# Self follow / unfollow has no effect
cases.append((
    ["Twitter", "postTweet", "follow", "getNewsFeed", "unfollow", "getNewsFeed", "postTweet", "getNewsFeed"],
    [[], [1, 10], [1, 1], [1], [1, 1], [1], [1, 11], [1]],
    [None, None, None, [10], None, [10], None, [11, 10]],
))

# Unfollow without following is a no-op
cases.append((
    ["Twitter", "postTweet", "unfollow", "getNewsFeed"],
    [[], [1, 3], [1, 2], [1]],
    [None, None, None, [3]],
))

# Interleaved tweets from multiple followees
cases.append((
    ["Twitter", "postTweet", "postTweet", "postTweet", "postTweet", "follow", "follow", "getNewsFeed"],
    [[], [1, 1], [2, 2], [3, 3], [1, 4], [1, 2], [1, 3], [1]],
    [None, None, None, None, None, None, None, [4, 3, 2, 1]],
))

# Follow is directional
cases.append((
    ["Twitter", "postTweet", "postTweet", "follow", "getNewsFeed", "getNewsFeed"],
    [[], [1, 7], [2, 8], [1, 2], [2], [1]],
    [None, None, None, None, [8], [8, 7]],
))

# Tweet id 0 and re-follow after unfollow
cases.append((
    ["Twitter", "postTweet", "postTweet", "follow", "unfollow", "follow", "getNewsFeed", "follow", "getNewsFeed"],
    [[], [2, 0], [1, 5], [1, 2], [1, 2], [1, 2], [1], [1, 2], [1]],
    [None, None, None, None, None, None, [5, 0], None, [5, 0]],
))

# Tweets posted before following are visible after following; 10 cap across users
ops = ["Twitter"]
args = [[]]
tid = 0
for u in range(2, 8):
    for _ in range(3):
        ops.append("postTweet")
        args.append([u, tid])
        tid += 1
for u in range(2, 8):
    ops.append("follow")
    args.append([1, u])
ops.append("getNewsFeed")
args.append([1])
cases.append((ops, args, None))

# Unfollow removes older tweets from feed
cases.append((
    ["Twitter", "postTweet", "postTweet", "postTweet", "follow", "follow", "unfollow", "getNewsFeed"],
    [[], [1, 1], [2, 2], [3, 3], [1, 2], [1, 3], [1, 2], [1]],
    [None, None, None, None, None, None, None, [3, 1]],
))

# Large input for performance
import random
random.seed(12345)
ops = ["Twitter"]
args = [[]]
next_tweet = 0
for _ in range(29990):
    r = random.random()
    if r < 0.4 and next_tweet <= 10000:
        ops.append("postTweet")
        args.append([random.randint(1, 500), next_tweet])
        next_tweet += 1
    elif r < 0.65:
        ops.append("follow")
        args.append([random.randint(1, 500), random.randint(1, 500)])
    elif r < 0.75:
        ops.append("unfollow")
        args.append([random.randint(1, 500), random.randint(1, 500)])
    else:
        ops.append("getNewsFeed")
        args.append([random.randint(1, 500)])
cases.append((ops, args, None))

passed = 0
total = len(cases)
for i, (ops, args, expected) in enumerate(cases, 1):
    if expected is None:
        expected = brute_force(ops, args)
    try:
        got = run_ops(ops, args)
        ok = got == expected
    except Exception as e:
        print(f"FAIL case {i}: input=({ops if len(ops) < 30 else '<%d ops>' % len(ops)}), error={type(e).__name__}: {e}")
        continue
    if ok:
        passed += 1
        print(f"PASS case {i}")
    else:
        if len(ops) < 30:
            print(f"FAIL case {i}: input=({ops}, {args}), expected={expected}, got={got}")
        else:
            idx = next((j for j, (a, b) in enumerate(zip(got, expected)) if a != b), -1)
            print(f"FAIL case {i}: input=<{len(ops)} ops>, first mismatch at op {idx} "
                  f"({ops[idx]} {args[idx]}), expected={expected[idx]}, got={got[idx]}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)