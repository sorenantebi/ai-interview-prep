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
    q = [root]
    i = 1
    while q and i < len(arr):
        n = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            n.left = TreeNode(arr[i])
            q.append(n.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            n.right = TreeNode(arr[i])
            q.append(n.right)
        i += 1
    return root


def tree_to_array(root):
    out = []
    q = [root]
    while q:
        n = q.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    ([[1, 2], [2, 3], [6, 1]], [2, 5, 5]),
    ([[100, 100], [200, 100]], [100, 100]),
    ([[1, 1]], [1]),
    ([[1, 1], [1, 1], [1, 1]], [1, 2, 3]),
    ([[1, 5], [2, 2], [3, 1]], [5, 7, 8]),
    ([[1, 2], [3, 2], [5, 2]], [2, 2, 2]),
    ([[4, 6], [1, 2], [2, 3]], [6, 6, 9]),
    ([[9, 7], [1, 9], [3, 1]], [7, 16, 17]),
    ([[6, 1], [9, 2], [2, 4]], [1, 2, 4]),
    ([[100000000, 1000000], [99500000, 1000000]], [1000000, 2000000]),
    ([[1, 1], [1, 2], [1, 3]], [1, 3, 6]),
    ([[1, 3], [3, 3], [5, 3]], [3, 6, 9]),
    ([[1, 1]] * 1000, list(range(1, 1001))),
    ([[2 * i + 1, 1] for i in range(1000)], [1] * 1000),
]

passed = 0
total = len(cases)
for n, (positions, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.fallingSquares([list(p) for p in positions])
        if list(got) == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            shown = positions if len(positions) <= 10 else f"<{len(positions)} positions>"
            exp_s = expected if len(expected) <= 10 else f"<{len(expected)} values>"
            got_s = got if got is None or len(got) <= 10 else f"<{len(got)} values>"
            print(f"FAIL case {n}: input={shown}, expected={exp_s}, got={got_s}")
    except Exception as e:
        print(f"FAIL case {n}: input=<{len(positions)} positions>, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)