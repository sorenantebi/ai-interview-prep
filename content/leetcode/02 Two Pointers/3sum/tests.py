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


def canon(res):
    return sorted(tuple(sorted(t)) for t in res)


def brute(nums):
    n = len(nums)
    found = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    found.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return sorted(found)


def fast_expected(nums):
    s = sorted(nums)
    found = set()
    n = len(s)
    for i in range(n):
        if i and s[i] == s[i - 1]:
            continue
        seen = set()
        for j in range(i + 1, n):
            c = -s[i] - s[j]
            if c in seen:
                found.add(tuple(sorted((s[i], s[j], c))))
            seen.add(s[j])
    return sorted(found)


rng = random.Random(12345)
rand_small = [rng.randint(-10, 10) for _ in range(30)]
rand_large = [rng.randint(-100000, 100000) for _ in range(3000)]
many_zero_mix = [0] * 1500 + [rng.randint(-5, 5) for _ in range(1500)]

cases = [
    [-1, 0, 1, 2, -1, -4],
    [0, 1, 1],
    [0, 0, 0],
    [1, 2, 3],
    [-1, -2, -3],
    [0, 0, 0, 0, 0, 0],
    [-2, 0, 1, 1, 2],
    [-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6],
    [3, -1, -2, 0, 0, 5, -5, 2, -3, 1],
    [100000, -100000, 0, 100000, -100000],
    rand_small,
    list(range(-1500, 1500)),
    many_zero_mix,
    rand_large,
]

passed = 0
total = len(cases)
for idx, nums in enumerate(cases, 1):
    inp = list(nums)
    if len(inp) <= 40:
        expected = brute(inp)
    else:
        expected = fast_expected(inp)
    shown = inp if len(inp) <= 40 else f"<list of {len(inp)} ints>"
    try:
        sol = ns["Solution"]()
        got = sol.threeSum(list(nums))
        got_c = canon(got)
        # duplicates must not appear and every triplet must be valid
        ok = (
            got_c == expected
            and len(got_c) == len(got)
            and all(len(t) == 3 and sum(t) == 0 for t in got)
        )
        if ok:
            passed += 1
            print(f"PASS case {idx}")
        else:
            exp_show = expected if len(expected) <= 20 else f"<{len(expected)} triplets>"
            got_show = got_c if len(got_c) <= 20 else f"<{len(got_c)} triplets>"
            print(f"FAIL case {idx}: input={shown}, expected={exp_show}, got={got_show}")
    except Exception as e:
        print(f"FAIL case {idx}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)