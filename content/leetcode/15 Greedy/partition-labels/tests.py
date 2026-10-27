import sys
import string
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

alphabet = string.ascii_lowercase

cases = [
    ("ababcbacadefegdehijhklij", [9, 7, 8]),
    ("eccbbbbdec", [10]),
    ("abc", [1, 1, 1]),
    ("a", [1]),
    ("aaaa", [4]),
    ("abab", [4]),
    ("abcabc", [6]),
    ("aabbcc", [2, 2, 2]),
    ("abacbd", [5, 1]),
    ("caedbdedda", [1, 9]),
    ("a" * 250 + "b" * 250, [250, 250]),
    (alphabet * 19, [len(alphabet * 19)]),
    (alphabet, [1] * 26),
]

passed = 0
total = len(cases)
for n, (s, expected) in enumerate(cases, 1):
    shown = s if len(s) <= 60 else s[:57] + "..."
    try:
        got = ns["Solution"]().partitionLabels(s)
        if list(got) == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            exp_shown = expected if len(expected) <= 30 else str(expected[:30]) + "..."
            print(f"FAIL case {n}: input={shown!r}, expected={exp_shown}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={shown!r}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
