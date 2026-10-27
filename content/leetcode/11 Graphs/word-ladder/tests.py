import sys
import random
import collections
from collections import deque
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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional,
      "Dict": Dict, "collections": collections, "deque": deque}
exec(open("attempt.py").read(), ns)


def make_large_path():
    rng = random.Random(1)
    n = 10
    path = []
    for i in range(1, n + 1):
        path.append("b" * i + "a" * (n - i))
    words = set(path)
    while len(words) < 5000:
        w = "".join(rng.choice("abc") for _ in range(n))
        if w != "a" * n:
            words.add(w)
    words = sorted(words)
    rng.shuffle(words)
    return "a" * n, "b" * n, words


def make_large_unreachable():
    rng = random.Random(2)
    n = 10
    words = {"z" * n}
    while len(words) < 5000:
        words.add("".join(rng.choice("abc") for _ in range(n)))
    words = sorted(words)
    rng.shuffle(words)
    return "a" * n, "z" * n, words


lp_b, lp_e, lp_w = make_large_path()
lu_b, lu_e, lu_w = make_large_unreachable()
dense = [chr(97 + i) + chr(97 + j) for i in range(26) for j in range(26) if (i, j) != (0, 0)]

cases = [
    ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"], 5),
    ("hit", "cog", ["hot", "dot", "dog", "lot", "log"], 0),
    ("a", "c", ["a", "b", "c"], 2),
    ("abc", "xyz", ["abd", "xyz"], 0),
    ("hot", "dot", ["dot"], 2),
    ("hit", "cog", ["hit", "hot", "dot", "dog", "cog"], 5),
    ("red", "tax", ["ted", "tex", "red", "tax", "tad", "den", "rex", "pee"], 4),
    ("leet", "code", ["lest", "leet", "lose", "code", "lode", "robe", "lost"], 6),
    ("a", "e", ["b", "c", "d", "e"], 2),
    ("aa", "zz", dense, 3),
    (lp_b, lp_e, lp_w, 11),
    (lu_b, lu_e, lu_w, 0),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 150 else s[:147] + "..."


passed = 0
total = len(cases)
for idx, (b, e, wl, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().ladderLength(b, e, list(wl))
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={short((b, e, wl))}, expected={expected}, got={got}")
    except Exception as ex:
        print(f"FAIL case {idx}: input={short((b, e, wl))}, expected={expected}, got=error: {type(ex).__name__}: {ex}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
