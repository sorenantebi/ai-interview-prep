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
    nodes = []
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
        nodes.append(cur)
    return dummy.next, nodes


def list_to_array(head, limit=100000):
    out = []
    seen = 0
    while head is not None:
        out.append(head.val)
        head = head.next
        seen += 1
        if seen > limit:
            raise RuntimeError("cycle detected or list too long")
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]


def expected_result(values, k):
    out = []
    n = len(values)
    i = 0
    while i + k <= n:
        out.extend(reversed(values[i:i + k]))
        i += k
    out.extend(values[i:])
    return out


CASES = [
    ([1, 2, 3, 4, 5], 2),
    ([1, 2, 3, 4, 5], 3),
    ([1], 1),
    ([1, 2], 2),
    ([1, 2, 3, 4], 1),
    ([1, 2, 3, 4, 5], 5),
    ([1, 2, 3, 4, 5, 6], 3),
    ([1, 2, 3, 4, 5, 6, 7], 3),
    ([5, 5, 5, 5, 5], 2),
    ([0, 1000, 0, 1000, 7, 8, 9], 4),
    (list(range(10)), 10),
    (list(range(1000)) * 5, 7),
    (list(range(5000)), 2),
    (list(range(5000)), 5000),
]


def main():
    passed = 0
    total = len(CASES)
    for idx, (values, k) in enumerate(CASES, 1):
        exp = expected_result(values, k)
        shown = values if len(values) <= 20 else f"<list of {len(values)} items>"
        shown_exp = exp if len(exp) <= 20 else f"<list of {len(exp)} items>"
        try:
            head, nodes = build_list(values)
            res = Solution().reverseKGroup(head, k)
            got = list_to_array(res)
            ok = got == exp
            # nodes must be relinked, not values rewritten
            if ok:
                orig_ids = {id(n) for n in nodes}
                cur = res
                while cur is not None:
                    if id(cur) not in orig_ids:
                        ok = False
                        break
                    cur = cur.next
            if ok:
                passed += 1
                print(f"PASS case {idx}")
            else:
                shown_got = got if len(got) <= 20 else f"<list of {len(got)} items>"
                print(f"FAIL case {idx}: input=(head={shown}, k={k}), expected={shown_exp}, got={shown_got}")
        except Exception as e:
            print(f"FAIL case {idx}: input=(head={shown}, k={k}), expected={shown_exp}, got=error: {e!r}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()
