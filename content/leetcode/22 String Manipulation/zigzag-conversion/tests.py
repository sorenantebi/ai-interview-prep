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


def build_list(arr):
    head = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head


def list_to_arr(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = [root]
    i = 1
    while q and i < len(arr):
        n = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            n.left = TreeNode(arr[i])
            q.append(n.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            n.right = TreeNode(arr[i])
            q.append(n.right)
        i += 1
    return root


def tree_to_arr(root):
    if not root:
        return []
    out = []
    q = [root]
    while q:
        n = q.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


def jump_reference(s, n):
    # independent cycle-based computation, used only for the large case
    if n == 1:
        return s
    cyc = 2 * (n - 1)
    res = []
    for row in range(n):
        i = row
        while i < len(s):
            res.append(s[i])
            if 0 < row < n - 1:
                j = i + cyc - 2 * row
                if j < len(s):
                    res.append(s[j])
            i += cyc
    return "".join(res)


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

big = "".join("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,."[i % 54] for i in range(1000))

cases = [
    ("PAYPALISHIRING", 3, "PAHNAPLSIIGYIR"),
    ("PAYPALISHIRING", 4, "PINALSIGYAHRPI"),
    ("A", 1, "A"),
    ("AB", 1, "AB"),
    ("AB", 2, "AB"),
    ("ABC", 2, "ACB"),
    ("ABCDE", 2, "ACEBD"),
    ("ABCDE", 3, "AEBDC"),
    ("ABCDEFGH", 1000, "ABCDEFGH"),
    ("abcdefghij", 4, "agbfhceidj"),
    ("A,B.c", 2, "ABc,."),
    (big, 7, jump_reference(big, 7)),
    (big, 1000, big),
    (big, 2, big[0::2] + big[1::2]),
]


def run():
    passed = 0
    total = len(cases)
    for idx, (s, n, expected) in enumerate(cases, 1):
        try:
            sol = ns["Solution"]()
            got = sol.convert(s, n)
            if got == expected:
                print(f"PASS case {idx}")
                passed += 1
            else:
                shown = s if len(s) <= 40 else s[:40] + "..."
                exp = expected if len(expected) <= 40 else expected[:40] + "..."
                g = got if not isinstance(got, str) or len(got) <= 40 else got[:40] + "..."
                print(f"FAIL case {idx}: input=({shown!r}, {n}), expected={exp!r}, got={g!r}")
        except Exception as e:
            print(f"FAIL case {idx}: input=({s[:40]!r}, {n}), error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()