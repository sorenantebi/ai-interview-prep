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


def expected_result(nums):
    n = len(nums)
    res = [1] * n
    p = 1
    for i in range(n):
        res[i] = p
        p *= nums[i]
    s = 1
    for i in range(n - 1, -1, -1):
        res[i] *= s
        s *= nums[i]
    return res


def short(x):
    s = repr(x)
    return s if len(s) <= 120 else s[:117] + "..."


def make_large_ones():
    return [1] * 100000


def make_large_two_zeros():
    nums = [(i % 7) - 3 or 2 for i in range(100000)]
    nums[10] = 0
    nums[99990] = 0
    return nums


def make_large_signs():
    # products stay within +/-1 except a few 2s, so they fit in 32 bits
    nums = [1 if i % 2 == 0 else -1 for i in range(100000)]
    nums[0] = 2
    nums[50000] = 3
    return nums


cases = [
    [1, 2, 3, 4],
    [-1, 1, 0, -3, 3],
    [2, 5],
    [0, 0],
    [0, 4],
    [0, 4, 5],
    [0, 0, 3, 4],
    [-2, -3],
    [1, 1, 1, 1, 1],
    [-30, 30, -1, 1],
    [5, 5, 5, 5],
    make_large_ones(),
    make_large_two_zeros(),
    make_large_signs(),
]

passed = 0
total = len(cases)
for idx, nums in enumerate(cases, 1):
    exp = expected_result(nums)
    try:
        start = time.time()
        got = ns["Solution"]().productExceptSelf(list(nums))
        elapsed = time.time() - start
        got = list(got)
        if got == exp:
            if elapsed > 5:
                print(f"FAIL case {idx}: input={short(nums)}, too slow ({elapsed:.2f}s)")
            else:
                print(f"PASS case {idx}")
                passed += 1
        else:
            print(f"FAIL case {idx}: input={short(nums)}, expected={short(exp)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {idx}: input={short(nums)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)