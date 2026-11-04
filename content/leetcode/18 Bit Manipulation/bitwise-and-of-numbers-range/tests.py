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


def list_to_py(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

CASES = [
    ((5, 7), 4),
    ((0, 0), 0),
    ((1, 2147483647), 0),
    ((1, 1), 1),
    ((2147483647, 2147483647), 2147483647),
    ((0, 1), 0),
    ((6, 7), 6),
    ((12, 15), 12),
    ((3, 4), 0),
    ((10, 11), 10),
    ((2147483646, 2147483647), 2147483646),
    ((1073741824, 2147483647), 1073741824),
    ((2147483640, 2147483647), 2147483640),
]


def main():
    passed = 0
    total = len(CASES)
    for i, (args, expected) in enumerate(CASES, 1):
        try:
            got = ns["Solution"]().rangeBitwiseAnd(*args)
            if got == expected:
                print(f"PASS case {i}")
                passed += 1
            else:
                print(f"FAIL case {i}: input={args}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {i}: input={args}, expected={expected}, got=exception: {e!r}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()
