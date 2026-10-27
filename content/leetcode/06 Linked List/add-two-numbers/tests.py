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
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head):
    out = []
    seen = 0
    while head is not None:
        out.append(head.val)
        head = head.next
        seen += 1
        if seen > 100000:
            raise RuntimeError("list too long (possible cycle)")
    return out


def num_to_digits(n):
    return [int(c) for c in reversed(str(n))]


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]


def make_case(a, b):
    return (a, b, num_to_digits(int("".join(map(str, reversed(a)))) + int("".join(map(str, reversed(b))))))


cases = [
    ([2, 4, 3], [5, 6, 4], [7, 0, 8]),
    ([0], [0], [0]),
    ([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9], [8, 9, 9, 9, 0, 0, 0, 1]),
    ([1], [2], [3]),
    ([5], [5], [0, 1]),
    ([9], [1], [0, 1]),
    ([1, 8], [0], [1, 8]),
    ([0], [7, 3], [7, 3]),
    ([9, 9], [1], [0, 0, 1]),
    ([1, 2, 3], [9, 8, 7], [0, 1, 1, 1]),
    make_case([9] * 100, [1]),
    make_case([9] * 100, [9] * 100),
    make_case([(i * 7) % 10 for i in range(99)] + [1], [(i * 3) % 10 for i in range(60)] + [4]),
]

passed = 0
total = len(cases)
for i, (a, b, expected) in enumerate(cases, 1):
    try:
        res = Solution().addTwoNumbers(build_list(a), build_list(b))
        got = list_to_array(res)
        if got == expected:
            passed += 1
            print(f"PASS case {i}")
        else:
            print(f"FAIL case {i}: input=l1={a}, l2={b}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input=l1={a}, l2={b}, expected={expected}, got=exception: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)