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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    ("abc", "pqr", "apbqcr"),
    ("ab", "pqrs", "apbqrs"),
    ("abcd", "pq", "apbqcd"),
    ("a", "b", "ab"),
    ("a", "pqrst", "apqrst"),
    ("abcde", "p", "apbcde"),
    ("aaa", "aaa", "aaaaaa"),
    ("xyz", "xyz", "xxyyzz"),
    ("abcdefghij", "kl", "akblcdefghij"),
    ("a" * 100, "b" * 100, "ab" * 100),
    ("a" * 100, "b", "ab" + "a" * 99),
    ("a", "b" * 100, "ab" + "b" * 99),
]


def short(s):
    return s if len(s) <= 40 else s[:37] + "..."


passed = 0
for n, (w1, w2, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().mergeAlternately(w1, w2)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input=({short(w1)!r}, {short(w2)!r}), expected={short(expected)!r}, got={short(str(got))!r}")
    except Exception as e:
        print(f"FAIL case {n}: input=({short(w1)!r}, {short(w2)!r}), error={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)