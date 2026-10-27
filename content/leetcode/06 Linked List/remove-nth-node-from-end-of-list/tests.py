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


def build_list(values):
    dummy = ListNode(0)
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head, limit=1000):
    out = []
    while head is not None and len(out) <= limit:
        out.append(head.val)
        head = head.next
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def run(head, n):
    return ns["Solution"]().removeNthFromEnd(head, n)


CASES = [
    # (list values, n, expected)
    ([1, 2, 3, 4, 5], 2, [1, 2, 3, 5]),          # example 1
    ([1], 1, []),                                  # example 2
    ([1, 2], 1, [1]),                              # example 3
    ([1, 2], 2, [2]),                              # remove head of two
    ([1, 2, 3, 4, 5], 5, [2, 3, 4, 5]),            # remove head
    ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4]),            # remove tail
    ([1, 2, 3], 2, [1, 3]),                        # remove middle
    ([7, 7, 7, 7], 2, [7, 7, 7]),                  # duplicates
    ([0, 0], 1, [0]),                              # zero values
    ([5, 1, 5, 1, 5], 3, [5, 1, 1, 5]),            # duplicates, middle
    (list(range(30)), 1, list(range(29))),         # max size, tail
    (list(range(30)), 30, list(range(1, 30))),     # max size, head
    (list(range(30)), 15, list(range(0, 15)) + list(range(16, 30))),  # max size, middle
    ([100, 0, 100], 3, [0, 100]),                  # boundary values
]


def main():
    passed = 0
    total = len(CASES)
    for i, (values, n, expected) in enumerate(CASES, 1):
        try:
            got = list_to_array(run(build_list(values), n))
            if got == expected:
                passed += 1
                print(f"PASS case {i}")
            else:
                print(f"FAIL case {i}: input={(values, n)}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {i}: input={(values, n)}, expected={expected}, got=error: {type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()
