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


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    # (arr, k, x, expected)
    ([1, 2, 3, 4, 5], 4, 3, [1, 2, 3, 4]),
    ([1, 1, 2, 3, 4, 5], 4, -1, [1, 1, 2, 3]),
    ([5], 1, 100, [5]),
    ([1, 2, 3, 4, 5], 2, 10, [4, 5]),
    ([1, 3], 1, 2, [1]),
    ([1, 1, 1, 10, 10, 10], 1, 9, [10]),
    ([-5, -3, -1, 2, 4], 3, -2, [-5, -3, -1]),
    ([1, 2, 3], 3, 2, [1, 2, 3]),
    ([0, 0, 1, 2, 3, 3, 4, 7, 7, 8], 3, 5, [3, 3, 4]),
    ([1, 10, 15, 25, 35, 45, 50, 59], 1, 30, [25]),
    (list(range(10000)), 5000, 0, list(range(0, 5000))),
    (list(range(10000)), 1000, 5000, list(range(4500, 5500))),
    (list(range(10000)), 3, 10000, [9997, 9998, 9999]),
]


def short(v):
    s = repr(v)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
total = len(cases)
for i, (arr, k, x, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.findClosestElements(list(arr), k, x)
        got = list(got) if got is not None else got
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=(arr={short(arr)}, k={k}, x={x}), expected={short(expected)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {i}: input=(arr={short(arr)}, k={k}, x={x}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)