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
    ([1, 2, 3], 4, 7),
    ([9], 3, 0),
    ([1], 1, 1),
    ([1], 1000, 1),
    ([2], 5, 0),
    ([2], 6, 1),
    ([1, 2], 4, 5),
    ([1, 2], 10, 89),
    ([3, 5], 8, 2),
    ([1, 2, 3], 10, 274),
    ([5, 10, 20], 20, 6),
    ([3, 1, 2], 4, 7),
    ([1000], 1000, 1),
    (list(range(1, 201)), 2, 2),
]

passed = 0
total = len(cases)
for i, (nums, target, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().combinationSum4(list(nums), target)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=({nums if len(nums) < 20 else '...'}, {target}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input=({nums if len(nums) < 20 else '...'}, {target}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
