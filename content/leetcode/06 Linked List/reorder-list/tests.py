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
    nodes = []
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
        nodes.append(cur)
    return dummy.next, nodes


def serialize_list(head, limit):
    out = []
    while head is not None:
        out.append(head.val)
        if len(out) > limit:
            raise RuntimeError("list too long or contains a cycle")
        head = head.next
    return out


def expected_order(vals):
    res = []
    i, j = 0, len(vals) - 1
    while i <= j:
        res.append(vals[i])
        if i != j:
            res.append(vals[j])
        i += 1
        j -= 1
    return res


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    [1, 2, 3, 4],
    [1, 2, 3, 4, 5],
    [1],
    [1, 2],
    [1, 2, 3],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6, 7],
    [5, 5, 5, 5],
    [1000, 1, 1000, 1, 1000],
    [7, 3, 9, 3, 7, 1],
    [(i % 1000) + 1 for i in range(50000)],
    [(i % 1000) + 1 for i in range(49999)],
]


def short(vals):
    if len(vals) > 20:
        return f"<list of {len(vals)} values starting {vals[:10]}...>"
    return str(vals)


passed = 0
total = len(cases)
for n, vals in enumerate(cases, 1):
    exp = expected_order(vals)
    try:
        head, nodes = build_list(vals)
        sol = ns["Solution"]()
        sol.reorderList(head)
        got = serialize_list(head, len(vals))
        # nodes must be re-linked, not replaced or copied
        got_ids = []
        cur = head
        while cur is not None:
            got_ids.append(id(cur))
            cur = cur.next
        if sorted(got_ids) != sorted(id(x) for x in nodes):
            print(f"FAIL case {n}: input={short(vals)}, expected original nodes to be reused, got different node objects")
            continue
        if got == exp:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(vals)}, expected={short(exp)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(vals)}, expected={short(exp)}, got=exception {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)