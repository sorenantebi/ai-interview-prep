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


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
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


def brute(s):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
        best = max(best, len(seen))
    return best


import random

random.seed(12345)
rand_s = "".join(random.choice("abcde fg!1") for _ in range(200))

all_distinct = "".join(chr(33 + i) for i in range(90))

cases = [
    ("abcabcbb", 3),
    ("bbbbb", 1),
    ("pwwkew", 3),
    ("", 0),
    ("a", 1),
    ("au", 2),
    ("abba", 2),
    ("dvdf", 3),
    (" ", 1),
    ("a b a", 3),
    ("tmmzuxt", 5),
    (all_distinct, 90),
    (rand_s, brute(rand_s)),
    ("ab" * 25000, 2),
    ("".join(chr(33 + (i % 90)) for i in range(50000)), 90),
]


def run():
    passed = 0
    total = len(cases)
    for n, (s, expected) in enumerate(cases, 1):
        shown = s if len(s) <= 60 else s[:57] + "..."
        try:
            sol = ns["Solution"]()
            got = sol.lengthOfLongestSubstring(s)
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={shown!r}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input={shown!r}, expected={expected}, got=error: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()
