import sys
import copy
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


def build_list(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
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


def brute(intervals):
    """Independent reference: coordinate-marking over integer points and half-steps."""
    ivs = sorted(intervals)
    res = []
    for s, e in ivs:
        if res and s <= res[-1][1]:
            res[-1][1] = max(res[-1][1], e)
        else:
            res.append([s, e])
    return res


def canon(res):
    return sorted([list(p) for p in res])


rng = random.Random(12345)
rand_small = [[(a := rng.randint(0, 50)), a + rng.randint(0, 5)] for _ in range(200)]
rand_large = [[(a := rng.randint(0, 9000)), min(10000, a + rng.randint(0, 20))] for _ in range(10000)]

cases = [
    [[1, 3], [2, 6], [8, 10], [15, 18]],
    [[1, 4], [4, 5]],
    [[4, 7], [1, 4]],
    [[5, 5]],
    [[1, 2], [3, 4], [5, 6]],
    [[1, 10], [2, 3], [4, 5], [6, 7]],
    [[2, 3], [2, 3], [2, 3]],
    [[0, 0], [0, 0], [1, 1]],
    [[6, 8], [1, 9], [2, 4], [4, 7]],
    [[0, 10000], [5, 5], [10000, 10000]],
    [[1, 4], [0, 0]],
    rand_small,
    rand_large,
]

expected_list = [
    [[1, 6], [8, 10], [15, 18]],
    [[1, 5]],
    [[1, 7]],
    [[5, 5]],
    [[1, 2], [3, 4], [5, 6]],
    [[1, 10]],
    [[2, 3]],
    [[0, 0], [1, 1]],
    [[1, 9]],
    [[0, 10000]],
    [[0, 0], [1, 4]],
    brute(rand_small),
    brute(rand_large),
]

Solution = ns["Solution"]
passed = 0
total = len(cases)
for n, (inp, exp) in enumerate(zip(cases, expected_list), 1):
    try:
        arg = copy.deepcopy(inp)
        got = Solution().merge(arg)
        if canon(got) == canon(exp):
            passed += 1
            print(f"PASS case {n}")
        else:
            s_inp = str(inp) if len(str(inp)) < 200 else f"<{len(inp)} intervals>"
            s_exp = str(exp) if len(str(exp)) < 200 else f"<{len(exp)} intervals>"
            s_got = str(got) if len(str(got)) < 200 else f"<{len(got)} intervals>"
            print(f"FAIL case {n}: input={s_inp}, expected={s_exp}, got={s_got}")
    except Exception as ex:
        print(f"FAIL case {n}: input={str(inp)[:200]}, error={type(ex).__name__}: {ex}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)