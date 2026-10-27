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

cases = [
    ("aabcc", "dbbca", "aadbbcbcac", True),
    ("aabcc", "dbbca", "aadbbbaccc", False),
    ("", "", "", True),
    ("", "", "a", False),
    ("a", "", "a", True),
    ("", "b", "b", True),
    ("a", "b", "ab", True),
    ("a", "b", "ba", True),
    ("a", "b", "aa", False),
    ("ab", "", "ba", False),
    ("abc", "abc", "aabbcc", True),
    ("aa", "ab", "aaba", True),
    ("aa", "ab", "abaa", True),
    ("a" * 100, "a" * 100, "a" * 200, True),
    ("a" * 100, "a" * 100, "a" * 199 + "b", False),
]

passed = 0
total = len(cases)
for n, (s1, s2, s3, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().isInterleave(s1, s2, s3)
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            show = lambda s: s if len(s) <= 40 else s[:37] + "..."
            print(f"FAIL case {n}: input=({show(s1)!r}, {show(s2)!r}, {show(s3)!r}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input=({s1[:40]!r}, {s2[:40]!r}, {s3[:40]!r}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
