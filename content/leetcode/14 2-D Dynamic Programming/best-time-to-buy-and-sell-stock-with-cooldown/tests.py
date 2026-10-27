import sys
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


def build_list(vals):
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
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


def reference(prices):
    hold, sold, rest = float("-inf"), 0, 0
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

sys.setrecursionlimit(20000)

zigzag = [1000 if i % 2 else 0 for i in range(5000)]
rising_runs = [i % 100 * 10 for i in range(5000)]
pseudo = [(i * 7919 + 13) % 1001 for i in range(5000)]

cases = [
    ([1, 2, 3, 0, 2], 3),
    ([1], 0),
    ([2, 1], 0),
    ([1, 2], 1),
    ([1, 2, 4], 3),
    ([5, 4, 3, 2, 1], 0),
    ([1, 2, 3, 4, 5], 4),
    ([2, 1, 4], 3),
    ([1, 4, 2, 7], 6),
    ([6, 1, 6, 4, 3, 0, 2], 7),
    ([0, 0, 0, 0], 0),
    (zigzag, reference(zigzag)),
    (rising_runs, reference(rising_runs)),
    (pseudo, reference(pseudo)),
]


def short(x):
    s = str(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
total = len(cases)
for n, (prices, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().maxProfit(list(prices))
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(prices)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(prices)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)