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
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def reference(n):
    res = []
    cols = []

    def bt(r):
        if r == n:
            res.append(["." * c + "Q" + "." * (n - c - 1) for c in cols])
            return
        for c in range(n):
            if all(c != pc and abs(c - pc) != r - pr for pr, pc in enumerate(cols)):
                cols.append(c)
                bt(r + 1)
                cols.pop()

    bt(0)
    return res


def canon(sols):
    return sorted([list(s) for s in sols])


def valid_board(board, n):
    if not isinstance(board, list) or len(board) != n:
        return False
    pos = []
    for r, row in enumerate(board):
        if not isinstance(row, str) or len(row) != n:
            return False
        if row.count("Q") != 1 or row.count(".") != n - 1:
            return False
        pos.append((r, row.index("Q")))
    for i in range(n):
        for j in range(i + 1, n):
            (r1, c1), (r2, c2) = pos[i], pos[j]
            if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                return False
    return True


EX4 = [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]

CASES = [
    (4, EX4),
    (1, [["Q"]]),
    (2, []),
    (3, []),
    (5, reference(5)),
    (6, reference(6)),
    (7, reference(7)),
    (8, reference(8)),
    (9, reference(9)),
]

COUNTS = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}


def short(x, limit=300):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "...(%d chars)" % len(s)


passed = 0
total = 0

for n, expected in CASES:
    total += 1
    try:
        got = ns["Solution"]().solveNQueens(n)
        ok = (
            canon(got) == canon(expected)
            and len(got) == len(expected) == COUNTS[n]
            and all(valid_board(b, n) for b in got)
        )
        if ok:
            passed += 1
            print(f"PASS case {total}")
        else:
            print(f"FAIL case {total}: input=n={n}, expected={short(canon(expected))}, got={short(canon(got) if isinstance(got, list) else got)}")
    except Exception as e:
        print(f"FAIL case {total}: input=n={n}, error={type(e).__name__}: {e}")

# Case: no duplicate solutions for n=8 and result independent across repeated calls
total += 1
try:
    sol = ns["Solution"]()
    a = sol.solveNQueens(8)
    b = sol.solveNQueens(8)
    ok = len({tuple(x) for x in a}) == 92 and canon(a) == canon(b)
    if ok:
        passed += 1
        print(f"PASS case {total}")
    else:
        print(f"FAIL case {total}: input=n=8 repeated call, expected=92 distinct identical results, got={len({tuple(x) for x in a})} distinct, equal={canon(a) == canon(b)}")
except Exception as e:
    print(f"FAIL case {total}: input=n=8 repeated call, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)