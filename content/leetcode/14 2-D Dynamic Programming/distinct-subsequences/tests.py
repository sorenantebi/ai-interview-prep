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


def reference(s, t):
    dp = [1] + [0] * len(t)
    for c in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == c:
                dp[j] += dp[j - 1]
    return dp[len(t)]


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

CASES = [
    ("rabbbit", "rabbit", 3),
    ("babgbag", "bag", 5),
    ("a", "a", 1),
    ("a", "b", 0),
    ("abc", "abcd", 0),
    ("aaa", "aa", 3),
    ("abc", "abc", 1),
    ("AaAa", "Aa", 3),
    ("aaaaa", "aaa", 10),
    ("cba", "abc", 0),
    ("ab" * 25, "ab" * 6, reference("ab" * 25, "ab" * 6)),  # LeetCode guarantees the answer fits in 32 bits
    ("a" * 1000, "b", 0),
    ("a" * 1000, "a" * 1000, 1),
    ("abcde" * 20, "ace" * 4, reference("abcde" * 20, "ace" * 4)),
]


def main():
    passed = 0
    total = len(CASES)
    for n, (s, t, expected) in enumerate(CASES, 1):
        shown = f"s={s if len(s) <= 40 else s[:40] + '...'!r}, t={t if len(t) <= 40 else t[:40] + '...'!r}"
        try:
            got = ns["Solution"]().numDistinct(s, t)
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={shown}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input={shown}, expected={expected}, got=exception {type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()