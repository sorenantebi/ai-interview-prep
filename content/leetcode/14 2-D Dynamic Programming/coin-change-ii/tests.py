import sys
import time
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


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def serialize_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def serialize_tree(root):
    if not root:
        return []
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


sys.setrecursionlimit(100000)

ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]


def reference(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]


cases = [
    (5, [1, 2, 5], 4),                       # example 1
    (3, [2], 0),                             # example 2
    (10, [10], 1),                           # example 3
    (0, [7], 1),                             # amount 0 -> one way
    (0, [1, 2, 3], 1),                       # amount 0 with several coins
    (1, [1], 1),                             # single coin, single unit
    (3, [5, 10], 0),                         # all coins larger than amount
    (4, [3, 1, 2], 4),                       # unsorted coins
    (7, [2, 4], 0),                          # odd amount, even coins
    (500, [3, 5, 7, 8, 9, 10, 11], 35502874),  # known larger case
    (5000, [1], 1),                          # max amount, single coin
    (5000, [5000], 1),                       # max coin equals amount
    (5000, list(range(1000, 5001, 50)), None),  # performance: many coins, max amount
    (5000, [11, 24, 37, 50, 63, 76, 89, 102], None),  # performance: mixed coins
]

passed = 0
total = len(cases)
for idx, (amount, coins, expected) in enumerate(cases, 1):
    if expected is None:
        expected = reference(amount, list(coins))
    try:
        start = time.time()
        got = Solution().change(amount, list(coins))
        elapsed = time.time() - start
        if got == expected and elapsed < 10:
            print(f"PASS case {idx}")
            passed += 1
        elif got != expected:
            print(f"FAIL case {idx}: input=amount={amount}, coins={coins}, expected={expected}, got={got}")
        else:
            print(f"FAIL case {idx}: input=amount={amount}, coins={coins}, expected={expected}, got=too slow ({elapsed:.2f}s)")
    except Exception as e:
        print(f"FAIL case {idx}: input=amount={amount}, coins={coins}, expected={expected}, got=Exception: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)