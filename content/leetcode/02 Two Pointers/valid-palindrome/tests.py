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
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    while queue and i < len(arr):
        node = queue.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
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
    ("A man, a plan, a canal: Panama", True),
    ("race a car", False),
    (" ", True),
    ("a", True),
    ("ab", False),
    ("aa", True),
    ("0P", False),
    ("ab_a", True),
    ("_", True),
    (".,", True),
    ("12321", True),
    ("1a2", False),
    ("Able was I, ere I saw Elba!", True),
    ("a" * 100000 + "b" + "a" * 100000, True),
    ("a" * 100000 + "bc" + "a" * 100000, False),
]

passed = 0
total = len(cases)
for i, (s, expected) in enumerate(cases, 1):
    shown = s if len(s) <= 60 else s[:30] + "...(len=%d)" % len(s)
    try:
        got = ns["Solution"]().isPalindrome(s)
        if got == expected:
            passed += 1
            print(f"PASS case {i}")
        else:
            print(f"FAIL case {i}: input={shown!r}, expected={expected!r}, got={got!r}")
    except Exception as e:
        print(f"FAIL case {i}: input={shown!r}, expected={expected!r}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)