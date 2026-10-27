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


def rotate(arr, k):
    k %= len(arr)
    return arr[-k:] + arr[:-k] if k else arr[:]


big_sorted = list(range(-2500, 2500))
cases = [
    [3, 4, 5, 1, 2],
    [4, 5, 6, 7, 0, 1, 2],
    [11, 13, 15, 17],
    [1],
    [2, 1],
    [1, 2],
    [2, 3, 1],
    [3, 1, 2],
    [-1, -5000, -3],
    [5000, -5000],
    rotate(big_sorted, 1),
    rotate(big_sorted, 2499),
    rotate(big_sorted, 5000),
    rotate(big_sorted, 1),
]
cases = cases[:-1] + [rotate(big_sorted, 3777)]

passed = 0
total = len(cases)
for i, nums in enumerate(cases, 1):
    expected = min(nums)
    shown = nums if len(nums) <= 20 else f"<list of {len(nums)} elements, first={nums[:3]}...>"
    try:
        start = time.time()
        got = ns["Solution"]().findMin(list(nums))
        elapsed = time.time() - start
        if got == expected and elapsed < 2:
            print(f"PASS case {i}")
            passed += 1
        elif got == expected:
            print(f"FAIL case {i}: input={shown}, expected={expected}, got={got} (too slow: {elapsed:.2f}s)")
        else:
            print(f"FAIL case {i}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={shown}, expected={expected}, got=exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)