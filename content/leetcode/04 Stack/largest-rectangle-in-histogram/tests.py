import sys
import random
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
    queue = [root]
    i = 1
    while queue and i < len(arr):
        node = queue.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def brute(heights):
    best = 0
    n = len(heights)
    for i in range(n):
        lo = hi = i
        while lo > 0 and heights[lo - 1] >= heights[i]:
            lo -= 1
        while hi < n - 1 and heights[hi + 1] >= heights[i]:
            hi += 1
        best = max(best, heights[i] * (hi - lo + 1))
    return best


random.seed(12345)
rand_small = [random.randint(0, 20) for _ in range(50)]
rand_med = [random.randint(0, 10000) for _ in range(300)]

cases = [
    ([2, 1, 5, 6, 2, 3], 10),
    ([2, 4], 4),
    ([2, 1, 2], 3),
    ([5], 5),
    ([0], 0),
    ([0, 0, 0], 0),
    ([3, 3, 3, 3], 12),
    ([1, 2, 3, 4, 5], 9),
    ([5, 4, 3, 2, 1], 9),
    ([2, 0, 2], 2),
    (rand_small, brute(rand_small)),
    (rand_med, brute(rand_med)),
    ([10000] * 100000, 10000 * 100000),
    (list(range(1, 100001)) if False else [i % 10001 for i in range(100000)],
     None),
]

# expected for the last large case: computed with a trusted O(n) stack routine
def fast(heights):
    stack = []
    best = 0
    for i, h in enumerate(heights + [0]):
        start = i
        while stack and stack[-1][1] >= h:
            j, hj = stack.pop()
            best = max(best, hj * (i - j))
            start = j
        stack.append((start, h))
    return best

cases[-1] = (cases[-1][0], fast(cases[-1][0]))

sol = ns["Solution"]()
passed = 0
total = len(cases)
for n, (heights, expected) in enumerate(cases, 1):
    shown = heights if len(heights) <= 20 else f"<list of {len(heights)}>"
    try:
        got = sol.largestRectangleArea(list(heights))
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={shown}, expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)