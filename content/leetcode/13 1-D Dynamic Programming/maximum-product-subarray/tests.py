import sys
import random
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


def brute(nums):
    best = nums[0]
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            best = max(best, p)
    return best


random.seed(12345)
rand_small = [random.randint(-4, 4) for _ in range(12)]

# Large input: values in {1,-1} so products stay in range; all ones except a few negatives
large = [1] * 20000
large[5000] = -1
large[15000] = -1
large2 = [-1] * 20000  # even count -> product 1
large3 = [random.choice([-1, 1, 1, 0]) for _ in range(20000)]

cases = [
    ([2, 3, -2, 4], 6),
    ([-2, 0, -1], 0),
    ([5], 5),
    ([-5], -5),
    ([0], 0),
    ([-2, -3], 6),
    ([-2, 3, -4], 24),
    ([0, 0, 0], 0),
    ([-1, -1, -1], 1),
    ([2, -5, -2, -4, 3], 24),
    ([-2, 0, -3, 4, -1], 12),
    ([1, 0, -1, 2, 3, -5, -2], 60),
    ([-10, -10, -10], 100),
    (rand_small, brute(rand_small)),
    (large, 1 if False else brute_large if False else None),
]
# compute expected for large inputs without O(n^2): use known structure
cases = cases[:-1]
cases.append((large, 20000 - 2 if False else None))
cases = cases[:-1]


def kadane_ref(nums):
    res = nums[0]
    cmax = cmin = nums[0]
    for x in nums[1:]:
        c = (x, x * cmax, x * cmin)
        cmax, cmin = max(c), min(c)
        res = max(res, cmax)
    return res


cases.append((large2, kadane_ref(large2)))
cases.append((large3, kadane_ref(large3)))

passed = 0
total = len(cases)
for idx, (nums, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 20 else f"<list of {len(nums)} ints>"
    try:
        sol = ns["Solution"]()
        got = sol.maxProduct(list(nums))
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
