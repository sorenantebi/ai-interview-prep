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
    ([1, 2, 1], [1, 2, 1, 1, 2, 1]),
    ([1, 3, 2, 1], [1, 3, 2, 1, 1, 3, 2, 1]),
    ([5], [5, 5]),
    ([1, 1, 1], [1, 1, 1, 1, 1, 1]),
    ([1000, 1], [1000, 1, 1000, 1]),
    ([1, 2], [1, 2, 1, 2]),
    ([3, 2, 1], [3, 2, 1, 3, 2, 1]),
    ([7, 7, 8, 8], [7, 7, 8, 8, 7, 7, 8, 8]),
    (list(range(1, 1001)), list(range(1, 1001)) * 2),
    ([1000] * 1000, [1000] * 2000),
]

passed = 0
total = len(cases)

for idx, (nums, expected) in enumerate(cases, 1):
    try:
        arg = list(nums)
        got = ns["Solution"]().getConcatenation(arg)
        if got is not None and list(got) == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            s_in = nums if len(nums) <= 20 else f"<list of length {len(nums)}>"
            s_exp = expected if len(expected) <= 40 else f"<list of length {len(expected)}>"
            s_got = got if got is None or len(got) <= 40 else f"<list of length {len(got)}>"
            print(f"FAIL case {idx}: input={s_in}, expected={s_exp}, got={s_got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={nums if len(nums) <= 20 else len(nums)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)