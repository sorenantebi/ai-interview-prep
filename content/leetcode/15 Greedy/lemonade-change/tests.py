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


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    ([5, 5, 5, 10, 20], True),
    ([5, 5, 10, 10, 20], False),
    ([5], True),
    ([10], False),
    ([20], False),
    ([5, 5, 5, 5, 20], True),
    ([5, 5, 10, 20], True),
    ([5, 10, 5, 10, 20], False),
    ([5, 5, 5, 10, 10, 20], True),
    ([5, 5, 5, 10, 20, 20], False),
    ([5, 5, 5, 5, 10, 20, 20], False),
    ([5] * 50000 + [10] * 50000, True),
    ([5] * 50000 + [20] * 16666, True),
    ([5] * 50000 + [20] * 16667, False),
]

passed = 0
total = len(cases)
for i, (bills, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().lemonadeChange(list(bills))
        if got is expected or (isinstance(got, bool) and got == expected):
            print(f"PASS case {i}")
            passed += 1
        else:
            shown = bills if len(bills) <= 20 else f"<list of {len(bills)} bills>"
            print(f"FAIL case {i}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        shown = bills if len(bills) <= 20 else f"<list of {len(bills)} bills>"
        print(f"FAIL case {i}: input={shown}, expected={expected}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
