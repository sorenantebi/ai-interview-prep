import sys
import collections
import heapq
import itertools
import math
import bisect
import functools
from collections import Counter, deque, defaultdict
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


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


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
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
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


def formula(tasks, n):
    c = Counter(tasks)
    mx = max(c.values())
    cnt = sum(1 for v in c.values() if v == mx)
    return max(len(tasks), (mx - 1) * (n + 1) + cnt)


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "Tuple": Tuple,
    "Set": Set,
    "collections": collections,
    "heapq": heapq,
    "itertools": itertools,
    "math": math,
    "bisect": bisect,
    "functools": functools,
    "Counter": Counter,
    "deque": deque,
    "defaultdict": defaultdict,
}
exec(open("attempt.py").read(), ns)

letters = [chr(ord("A") + i) for i in range(26)]

big1 = ["A"] * 5000 + ["B"] * 5000
big2 = [letters[i % 26] for i in range(10000)]
big3 = ["A"] * 10000
big4 = ["A"] * 3000 + ["B"] * 3000 + ["C"] * 2000 + ["D"] * 1000 + ["E"] * 1000

cases = [
    ((["A", "A", "A", "B", "B", "B"], 2), 8),
    ((["A", "C", "A", "B", "D", "B"], 1), 6),
    ((["A", "A", "A", "B", "B", "B"], 3), 10),
    ((["A"], 0), 1),
    ((["A"], 100), 1),
    ((["A", "A"], 100), 102),
    ((["A"] * 5, 0), 5),
    ((["A", "A", "A", "B", "B", "B"], 0), 6),
    ((list(letters), 100), 26),
    ((["A"] * 4 + ["B"] * 4, 1), 8),
    ((["A"] * 6 + ["B", "C", "D", "E", "F", "G"], 2), 16),
    ((big1, 100), 504901),
    ((big2, 100), formula(big2, 100)),
    ((big3, 100), 9999 * 101 + 1),
    ((big4, 50), formula(big4, 50)),
]


def describe(args):
    tasks, n = args
    if len(tasks) > 40:
        return f"(<{len(tasks)} tasks>, {n})"
    return f"({tasks}, {n})"


passed = 0
total = len(cases)
for idx, (args, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.leastInterval(list(args[0]), args[1])
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={describe(args)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={describe(args)}, expected={expected}, got=exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)