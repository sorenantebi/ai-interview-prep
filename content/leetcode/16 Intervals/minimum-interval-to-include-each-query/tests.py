import sys
import heapq
import bisect
import collections
import itertools
import math
import random
from typing import List, Optional, Dict, Tuple, Set


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
    q = collections.deque([root])
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
    out = []
    q = collections.deque([root])
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


def reference(intervals, queries):
    ivs = sorted(tuple(x) for x in intervals)
    heap = []
    res = {}
    i = 0
    for q in sorted(queries):
        while i < len(ivs) and ivs[i][0] <= q:
            l, r = ivs[i]
            heapq.heappush(heap, (r - l + 1, r))
            i += 1
        while heap and heap[0][1] < q:
            heapq.heappop(heap)
        res[q] = heap[0][0] if heap else -1
    return [res[q] for q in queries]


def brute(intervals, queries):
    out = []
    for q in queries:
        best = -1
        for l, r in intervals:
            if l <= q <= r:
                s = r - l + 1
                if best == -1 or s < best:
                    best = s
        out.append(best)
    return out


ns = {
    "ListNode": ListNode, "TreeNode": TreeNode, "List": List,
    "Optional": Optional, "Dict": Dict, "Tuple": Tuple, "Set": Set,
    "heapq": heapq, "bisect": bisect, "collections": collections,
    "itertools": itertools, "math": math, "random": random,
    "heappush": heapq.heappush, "heappop": heapq.heappop,
    "heapify": heapq.heapify,
    "deque": collections.deque, "defaultdict": collections.defaultdict,
    "Counter": collections.Counter,
    "bisect_left": bisect.bisect_left, "bisect_right": bisect.bisect_right,
}
exec(open("attempt.py").read(), ns)


def run(intervals, queries):
    return ns["Solution"]().minInterval(
        [list(x) for x in intervals], list(queries)
    )


def short(x):
    if isinstance(x, list) and len(x) > 30:
        return "<%d items>" % len(x)
    return repr(x)


rng = random.Random(12345)

cases = []
cases.append(([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5], [3, 3, 1, 4]))
cases.append(([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22], [2, -1, 4, 6]))
cases.append(([[1, 1]], [1], [1]))
cases.append(([[3, 7]], [2, 3, 5, 7, 8], [-1, 5, 5, 5, -1]))
cases.append(([[1, 3], [1, 3], [2, 2]], [2, 2, 3, 3, 1], [1, 1, 3, 3, 3]))
cases.append(([[10, 20], [1, 100], [5, 15], [12, 12]], [12, 100, 1, 16, 21, 50],
              [1, 100, 100, 11, 100, 100]))
cases.append(([[1, 2], [5, 6], [9, 10]], [3, 4, 7, 8, 11], [-1, -1, -1, -1, -1]))
cases.append(([[1, 10000000], [9999999, 10000000]], [1, 9999998, 9999999, 10000000],
              [10000000, 10000000, 2, 2]))
cases.append(([[1, 3], [2, 4], [3, 5]], [1, 2, 3, 4, 5, 6], [3, 3, 3, 3, 3, -1]))

for n, m, hi in ((18, 28, 60), (9, 6, 55)):
    ivs = []
    for _ in range(n):
        a = rng.randint(1, hi)
        b = rng.randint(a, min(hi, a + 50))
        ivs.append([a, b])
    qs = [rng.randint(1, hi + 10) for _ in range(m)]
    cases.append((ivs, qs, brute(ivs, qs)))

big_iv = []
for _ in range(100000):
    a = rng.randint(1, 10000000)
    b = min(10000000, a + rng.randint(0, 1000000))
    big_iv.append([a, b])
big_q = [rng.randint(1, 10000000) for _ in range(100000)]
cases.append((big_iv, big_q, reference(big_iv, big_q)))

passed = 0
total = len(cases)
for idx, (ivs, qs, expected) in enumerate(cases, 1):
    try:
        got = run(ivs, qs)
        if list(got) == expected:
            print("PASS case %d" % idx)
            passed += 1
        else:
            print("FAIL case %d: input=intervals=%s, queries=%s, expected=%s, got=%s"
                  % (idx, short(ivs), short(qs), short(expected), short(got)))
    except Exception as e:
        print("FAIL case %d: input=intervals=%s, queries=%s, error=%s: %s"
              % (idx, short(ivs), short(qs), type(e).__name__, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)
