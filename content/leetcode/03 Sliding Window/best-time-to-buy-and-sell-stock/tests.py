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


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head):
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


def brute(prices):
    best = 0
    lo = prices[0]
    for p in prices:
        lo = min(lo, p)
        best = max(best, p - lo)
    return best


random.seed(12345)
rand_prices = [random.randint(0, 10000) for _ in range(1000)]
big_up = list(range(0, 10001)) + [10000] * 89999
big_down = list(range(10000, -1, -1)) * 9
big_down = big_down[:100000]
big_random = [random.randint(0, 10000) for _ in range(100000)]

cases = [
    ([7, 1, 5, 3, 6, 4], 5),
    ([7, 6, 4, 3, 1], 0),
    ([5], 0),
    ([1, 2], 1),
    ([2, 1], 0),
    ([3, 3, 3, 3], 0),
    ([0, 10000], 10000),
    ([10000, 0], 0),
    ([2, 4, 1], 2),
    ([3, 2, 6, 5, 0, 3], 4),
    ([1, 5, 0, 4], 4),
    (rand_prices, brute(rand_prices)),
    (big_up, 10000),
    (big_down, brute(big_down)),
    (big_random, brute(big_random)),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 100 else s[:97] + "..."


passed = 0
total = len(cases)
for n, (prices, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.maxProfit(list(prices))
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(prices)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(prices)}, expected={expected}, got=exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
