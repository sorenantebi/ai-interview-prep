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


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
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
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def reference(word1, word2):
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
        prev = cur
    return prev[n]


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

rng = random.Random(12345)
rand_a = "".join(rng.choice("abc") for _ in range(500))
rand_b = "".join(rng.choice("abc") for _ in range(500))

cases = [
    ("horse", "ros", 3),
    ("intention", "execution", 5),
    ("", "abc", 3),
    ("abc", "", 3),
    ("", "", 0),
    ("a", "a", 0),
    ("a", "b", 1),
    ("abc", "abc", 0),
    ("abc", "def", 3),
    ("kitten", "sitting", 3),
    ("sunday", "saturday", 3),
    ("a" * 500, "a" * 500, 0),
    ("a" * 500, "b" * 500, 500),
    ("a" * 500, "", 500),
    (rand_a, rand_b, reference(rand_a, rand_b)),
]


def short(s):
    return repr(s) if len(s) <= 40 else repr(s[:37] + "...") + f"(len={len(s)})"


passed = 0
for idx, (w1, w2, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().minDistance(w1, w2)
        if got == expected:
            passed += 1
            print(f"PASS case {idx}")
        else:
            print(f"FAIL case {idx}: input=({short(w1)}, {short(w2)}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input=({short(w1)}, {short(w2)}), expected={expected}, got=exception: {e!r}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)