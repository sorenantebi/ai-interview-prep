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

BIG = 100000
cases = [
    # (s, t, expected)
    ("ADOBECODEBANC", "ABC", "BANC"),
    ("a", "a", "a"),
    ("a", "aa", ""),
    ("ab", "b", "b"),
    ("aa", "aa", "aa"),
    ("abc", "cba", "abc"),
    ("aabbcc", "abc", "abbc"),
    ("bba", "ab", "ba"),
    ("ABCabc", "aA", "ABCa"),
    ("xyz", "a", ""),
    ("xaxbxaa", "aab", "bxaa"),
    ("ab", "abc", ""),
    ("A" + "x" * (BIG - 2) + "B", "AB", "A" + "x" * (BIG - 2) + "B"),
    ("a" * (BIG // 2) + "b" * (BIG // 2), "ab", "ab"),
    ("a" * BIG, "a" * (BIG // 2), "a" * (BIG // 2)),
]


def show(x):
    r = repr(x)
    return r if len(r) <= 60 else r[:57] + "..."


passed = 0
for i, (s, t, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().minWindow(s, t)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=({show(s)}, {show(t)}), expected={show(expected)}, got={show(got)}")
    except Exception as e:
        print(f"FAIL case {i}: input=({show(s)}, {show(t)}), expected={show(expected)}, got=exception: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
