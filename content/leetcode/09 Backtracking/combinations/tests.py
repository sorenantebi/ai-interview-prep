import sys
import math
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


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    out = []
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def canon(res):
    return sorted(tuple(sorted(c)) for c in res)


def exact(expected):
    exp = canon(expected)

    def check(got):
        return canon(got) == exp
    return check


def valid_count(n, k):
    total = math.comb(n, k)

    def check(got):
        if len(got) != total:
            return False
        seen = set()
        for c in got:
            if len(c) != k:
                return False
            t = tuple(sorted(c))
            if len(set(t)) != k or t[0] < 1 or t[-1] > n:
                return False
            seen.add(t)
        return len(seen) == total
    return check


# (n, k, checker, expected description)
cases = [
    (4, 2, exact([[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]),
     [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]),
    (1, 1, exact([[1]]), [[1]]),
    (3, 3, exact([[1, 2, 3]]), [[1, 2, 3]]),
    (3, 1, exact([[1], [2], [3]]), [[1], [2], [3]]),
    (3, 2, exact([[1, 2], [1, 3], [2, 3]]), [[1, 2], [1, 3], [2, 3]]),
    (5, 3, exact([[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5],
                  [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]]),
     "10 combinations of size 3 from 1..5"),
    (4, 3, exact([[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]),
     [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]),
    (5, 4, exact([[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5], [1, 3, 4, 5], [2, 3, 4, 5]]),
     [[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5], [1, 3, 4, 5], [2, 3, 4, 5]]),
    (2, 1, exact([[1], [2]]), [[1], [2]]),
    (20, 1, exact([[i] for i in range(1, 21)]), [[i] for i in range(1, 21)]),
    (20, 20, exact([list(range(1, 21))]), [list(range(1, 21))]),
    (20, 19, exact([[j for j in range(1, 21) if j != i] for i in range(1, 21)]),
     "20 combinations, each omitting one number"),
    (20, 10, valid_count(20, 10), "184756 unique valid combinations"),
]


def main():
    sol = ns["Solution"]()
    passed = 0
    total = len(cases)
    for idx, (n, k, check, expected) in enumerate(cases, 1):
        try:
            got = sol.combine(n, k)
            ok = check(got)
        except Exception as e:
            print(f"FAIL case {idx}: input=n={n}, k={k}, error={type(e).__name__}: {e}")
            continue
        if ok:
            passed += 1
            print(f"PASS case {idx}")
        else:
            shown = got if isinstance(got, list) and len(got) <= 30 else f"<{len(got) if hasattr(got, '__len__') else got} items>"
            print(f"FAIL case {idx}: input=n={n}, k={k}, expected={expected}, got={shown}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()