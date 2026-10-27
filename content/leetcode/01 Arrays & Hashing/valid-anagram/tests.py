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

big = "abcdefghijklmnopqrstuvwxyz" * 1923  # 49998 chars
big_rev = big[::-1]

cases = [
    ("listen", "silent", True),
    ("apple", "paple", True),
    ("car", "cat", False),
    ("a", "a", True),
    ("a", "b", False),
    ("a", "ab", False),
    ("ab", "a", False),
    ("aab", "abb", False),
    ("aabb", "bbaa", True),
    ("abcabc", "cbacba", True),
    ("rat", "tar", True),
    ("aaaa", "aaab", False),
    (big, big_rev, True),
    (big, big[:-1] + ("a" if big[-1] != "a" else "b"), False),
]

passed = 0
total = len(cases)

for n, (s, t, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().isAnagram(s, t)
        if got == expected and isinstance(got, bool):
            print(f"PASS case {n}")
            passed += 1
        else:
            ss = s if len(s) <= 40 else s[:40] + "..."
            ts = t if len(t) <= 40 else t[:40] + "..."
            print(f"FAIL case {n}: input=({ss!r}, {ts!r}), expected={expected}, got={got}")
    except Exception as e:
        ss = s if len(s) <= 40 else s[:40] + "..."
        ts = t if len(t) <= 40 else t[:40] + "..."
        print(f"FAIL case {n}: input=({ss!r}, {ts!r}), expected={expected}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)