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


class MountainArray:
    LIMIT = 100

    def __init__(self, arr):
        self._arr = arr
        self.calls = 0

    def get(self, index: int) -> int:
        self.calls += 1
        if self.calls > self.LIMIT:
            raise RuntimeError("more than 100 calls to MountainArray.get")
        if index < 0 or index >= len(self._arr):
            raise IndexError("index out of range: %d" % index)
        return self._arr[index]

    def length(self) -> int:
        return len(self._arr)


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional,
      "Dict": Dict, "MountainArray": MountainArray}
exec(open("attempt.py").read(), ns)

up = [2 * i for i in range(6000)]
down = [11997 - 2 * j for j in range(4000)]
big = up + down

cases = [
    ([1, 2, 3, 4, 5, 3, 1], 3, 2),
    ([0, 1, 2, 4, 2, 1], 3, -1),
    ([1, 2, 1], 1, 0),
    ([1, 2, 1], 2, 1),
    ([1, 2, 1], 3, -1),
    ([1, 5, 2], 2, 2),
    ([0, 1, 2, 3, 4, 5, 3, 1], 1, 1),
    ([1, 2, 3, 4, 5, 3, 1], 5, 4),
    ([0, 5, 3, 1], 1, 3),
    ([0, 1000000000, 5], 1000000000, 1),
    (big, 3999, 9999),
    (big, 4000, 2000),
    (big, 5001, 9498),
    (big, 11999, -1),
]

passed = 0
total = len(cases)
for i, (arr, target, expected) in enumerate(cases, 1):
    shown = arr if len(arr) <= 20 else "<array of length %d>" % len(arr)
    try:
        ma = MountainArray(arr)
        got = ns["Solution"]().findInMountainArray(target, ma)
        if got == expected:
            passed += 1
            print("PASS case %d" % i)
        else:
            print("FAIL case %d: input=(%s, target=%d), expected=%s, got=%s" % (i, shown, target, expected, got))
    except Exception as e:
        print("FAIL case %d: input=(%s, target=%d), expected=%s, got=error: %s" % (i, shown, target, expected, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)
