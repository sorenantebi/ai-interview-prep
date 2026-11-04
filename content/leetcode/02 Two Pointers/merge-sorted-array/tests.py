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
    q = [root]
    i = 1
    while q and i < len(arr):
        node = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

rng = random.Random(12345)
big1 = sorted(rng.randint(-10**9, 10**9) for _ in range(100))
big2 = sorted(rng.randint(-10**9, 10**9) for _ in range(100))
big_expected = sorted(big1 + big2)

# (nums1, m, nums2, n, expected)
CASES = [
    ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, [1, 2, 2, 3, 5, 6]),
    ([1], 1, [], 0, [1]),
    ([0], 0, [1], 1, [1]),
    ([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3, [1, 2, 3, 4, 5, 6]),
    ([1, 2, 3, 0, 0, 0], 3, [4, 5, 6], 3, [1, 2, 3, 4, 5, 6]),
    ([2, 2, 2, 0, 0], 3, [2, 2], 2, [2, 2, 2, 2, 2]),
    ([-5, -1, 0, 0, 0], 2, [-3, -2, 7], 3, [-5, -3, -2, -1, 7]),
    ([2, 0], 1, [1], 1, [1, 2]),
    ([10**9, 0, 0], 1, [-10**9, 10**9], 2, [-10**9, 10**9, 10**9]),
    ([0, 0, 0], 0, [1, 2, 3], 3, [1, 2, 3]),
    ([1, 3, 5, 7, 0, 0, 0, 0], 4, [2, 4, 6, 8], 4, [1, 2, 3, 4, 5, 6, 7, 8]),
    (big1 + [0] * 100, 100, big2, 100, big_expected),
]


def main():
    passed = 0
    total = len(CASES)
    for idx, (n1, m, n2, n, expected) in enumerate(CASES, 1):
        arg1 = list(n1)
        arg2 = list(n2)
        desc = f"nums1={n1 if len(n1) <= 12 else '<len %d>' % len(n1)}, m={m}, nums2={n2 if len(n2) <= 12 else '<len %d>' % len(n2)}, n={n}"
        try:
            sol = ns["Solution"]()
            sol.merge(arg1, m, arg2, n)
            if arg1 == expected:
                print(f"PASS case {idx}")
                passed += 1
            else:
                exp_s = expected if len(expected) <= 12 else f"<len {len(expected)}>"
                got_s = arg1 if len(arg1) <= 12 else f"<len {len(arg1)}>"
                print(f"FAIL case {idx}: input={desc}, expected={exp_s}, got={got_s}")
        except Exception as e:
            print(f"FAIL case {idx}: input={desc}, error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()