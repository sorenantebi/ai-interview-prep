import sys
import time
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


def serialize_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
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


def serialize_tree(root):
    if not root:
        return []
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]


def short(x, limit=200):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + f"... (len={len(x) if hasattr(x, '__len__') else '?'})"


cases = [
    ([1, 2, 3, 1], True),
    ([1, 2, 3, 4], False),
    ([5, 5, 6, 6, 7, 7], True),
    ([42], False),
    ([-1, -1], True),
    ([-10**9, 10**9, 0], False),
    ([0, 0], True),
    ([7, 7, 7, 7, 7], True),
    ([-3, -2, -1, 1, 2, 3], False),
    ([10**9, -10**9, 10**9], True),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 1], True),
    (list(range(100000)), False),
    (list(range(99999)) + [12345], True),
    ([-x for x in range(100000)], False),
]

passed = 0
total = len(cases)
for i, (nums, expected) in enumerate(cases, 1):
    arg = list(nums)
    try:
        start = time.time()
        got = Solution().containsDuplicate(arg)
        elapsed = time.time() - start
        if bool(got) == expected and isinstance(got, bool) or got == expected:
            if elapsed > 2.0:
                print(f"FAIL case {i}: input={short(nums)}, expected={expected}, got={got} (too slow: {elapsed:.2f}s)")
            else:
                print(f"PASS case {i}")
                passed += 1
        else:
            print(f"FAIL case {i}: input={short(nums)}, expected={expected}, got={got!r}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(nums)}, expected={expected}, got=Exception: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
