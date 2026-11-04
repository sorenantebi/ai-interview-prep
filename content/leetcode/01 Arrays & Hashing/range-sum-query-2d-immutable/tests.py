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
NumMatrix = ns["NumMatrix"]


def short(x, limit=200):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "...(truncated)"


cases = []

# 1: example 1
ex = [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]
cases.append((ex, [(2, 1, 4, 3), (1, 1, 2, 2), (1, 2, 2, 4)], [8, 11, 12]))

# 2: single cell
cases.append(([[5]], [(0, 0, 0, 0)], [5]))

# 3: single negative cell
cases.append(([[-7]], [(0, 0, 0, 0)], [-7]))

# 4: single row
cases.append(([[1, 2, 3, 4]], [(0, 1, 0, 2), (0, 0, 0, 3), (0, 3, 0, 3)], [5, 10, 4]))

# 5: single column
cases.append(([[1], [2], [3], [4]], [(1, 0, 2, 0), (0, 0, 3, 0), (3, 0, 3, 0)], [5, 10, 4]))

# 6: negatives 2x2
cases.append((
    [[-1, -2], [-3, -4]],
    [(0, 0, 1, 1), (0, 0, 0, 1), (1, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1)],
    [-10, -3, -7, -6, -4],
))

# 7: zeros
cases.append(([[0] * 3 for _ in range(3)], [(0, 0, 2, 2), (1, 1, 1, 1), (0, 1, 2, 2)], [0, 0, 0]))

# 8: 3x3 mixed
cases.append((
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    [(0, 0, 2, 2), (1, 1, 2, 2), (0, 0, 1, 1), (0, 1, 2, 1), (2, 0, 2, 2), (1, 0, 1, 2)],
    [45, 28, 12, 15, 24, 15],
))

# 9: example matrix, corners and full region, repeated queries
cases.append((
    ex,
    [(0, 0, 4, 4), (0, 0, 0, 0), (4, 4, 4, 4), (0, 0, 2, 2), (2, 1, 4, 3), (2, 1, 4, 3)],
    [58, 3, 5, 21, 8, 8],
))

# 10: large all-ones matrix, 10^4 queries, answer is the area
big = [[1] * 200 for _ in range(200)]
qs, exp = [], []
for k in range(10000):
    r1 = k % 200
    r2 = r1 + (k * 7) % (200 - r1)
    c1 = (k * 3) % 200
    c2 = c1 + (k * 11) % (200 - c1)
    qs.append((r1, c1, r2, c2))
    exp.append((r2 - r1 + 1) * (c2 - c1 + 1))
cases.append((big, qs, exp))

# 11: extreme values, full-matrix sums
cases.append((
    [[10000] * 200 for _ in range(200)],
    [(0, 0, 199, 199), (0, 0, 0, 0), (100, 100, 199, 199)],
    [400000000, 10000, 100 * 100 * 10000],
))
cases.append((
    [[-10000] * 200 for _ in range(200)],
    [(0, 0, 199, 199), (199, 199, 199, 199)],
    [-400000000, -10000],
))

# 13: checkerboard of +-10000
cb = [[10000 if (i + j) % 2 == 0 else -10000 for j in range(200)] for i in range(200)]
cases.append((
    cb,
    [(0, 0, 199, 199), (0, 0, 0, 0), (0, 1, 0, 1), (0, 0, 0, 1), (0, 0, 0, 2), (0, 0, 2, 2)],
    [0, 10000, -10000, 0, 10000, 10000],
))

passed = 0
total = len(cases)
for n, (matrix, queries, expected) in enumerate(cases, 1):
    try:
        obj = NumMatrix([row[:] for row in matrix])
        got = [obj.sumRegion(*q) for q in queries]
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input=matrix={short(matrix)}, queries={short(queries)}, "
                  f"expected={short(expected)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {n}: input=matrix={short(matrix)}, queries={short(queries)}, "
              f"error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)