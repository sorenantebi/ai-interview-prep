import sys
import heapq
import collections
from collections import Counter, defaultdict, deque
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


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "heapq": heapq,
    "collections": collections,
    "Counter": Counter,
    "defaultdict": defaultdict,
    "deque": deque,
}
exec(open("attempt.py").read(), ns)


def run(s):
    return ns["Solution"]().reorganizeString(s)


def valid(s, got, feasible):
    if not feasible:
        return got == ""
    if not isinstance(got, str):
        return False
    if sorted(got) != sorted(s):
        return False
    return all(got[i] != got[i + 1] for i in range(len(got) - 1))


# (input, feasible)
CASES = [
    ("aab", True),
    ("aaab", False),
    ("a", True),
    ("aa", False),
    ("ab", True),
    ("aabb", True),
    ("aaabc", True),
    ("aaaabc", False),
    ("vvvlo", True),
    ("zzzzyyyxx", True),
    ("abcdefghijklmnopqrstuvwxyz", True),
    ("a" * 250 + "b" * 250, True),
    ("a" * 251 + "b" * 249, False),
    ("a" * 250 + "bcdefghijklmnopqrstuvwxyz" * 10, True),
]


def short(s):
    return s if len(s) <= 40 else s[:37] + "..."


passed = 0
total = len(CASES)
for n, (s, feasible) in enumerate(CASES, 1):
    expected = "<any valid rearrangement>" if feasible else '""'
    try:
        got = run(s)
        if valid(s, got, feasible):
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(s)!r}, expected={expected}, got={short(got) if isinstance(got, str) else got!r}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(s)!r}, expected={expected}, got=error: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
