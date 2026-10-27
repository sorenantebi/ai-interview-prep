import sys
import traceback
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


def reference(candidates, target):
    cands = sorted(candidates)
    res, path = [], []

    def dfs(start, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(cands)):
            c = cands[i]
            if c > remaining:
                break
            path.append(c)
            dfs(i, remaining - c)
            path.pop()

    dfs(0, target)
    return res


def canonical(combos):
    return sorted(sorted(list(c)) for c in combos)


cases = [
    ([2, 3, 6, 7], 7, [[2, 2, 3], [7]]),
    ([2, 3, 5], 8, [[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
    ([2], 1, []),
    ([7], 7, [[7]]),
    ([2], 40, [[2] * 20]),
    ([8, 7, 4, 3], 11, [[3, 4, 4], [3, 8], [4, 7]]),
    ([40], 1, []),
    ([3, 5, 7], 1, []),
    ([5, 3], 9, [[3, 3, 3]]),
    (list(range(20, 41)), 40, [[20, 20], [40]]),
    ([5, 10, 15, 20, 25, 30, 35, 40], 40, None),
    ([7, 11, 13, 17, 19, 23, 29, 31, 37, 40, 9, 12, 14, 16, 18], 40, None),
    ([40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26,
      25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11], 40, None),
]

passed = 0
for n, (candidates, target, expected) in enumerate(cases, 1):
    if expected is None:
        expected = reference(candidates, target)
    try:
        got = Solution().combinationSum(list(candidates), target)
        ok = canonical(got) == canonical(expected)
    except Exception as e:
        got = f"Exception: {type(e).__name__}: {e}"
        ok = False
    if ok:
        passed += 1
        print(f"PASS case {n}")
    else:
        print(f"FAIL case {n}: input=(candidates={candidates}, target={target}), "
              f"expected={canonical(expected)}, got={got}")

total = len(cases)
print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)