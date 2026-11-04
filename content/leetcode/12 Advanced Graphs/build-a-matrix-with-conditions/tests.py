import sys
import random
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


def build_list(arr):
    head = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head


def list_to_arr(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = [root]
    i = 1
    while q and i < len(arr):
        node = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_arr(root):
    if not root:
        return []
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


def validate(k, rows, cols, got):
    """Return None if got is a valid matrix, else an error string."""
    if not isinstance(got, list) or len(got) != k:
        return "matrix must have k rows"
    pos = {}
    for r, row in enumerate(got):
        if not isinstance(row, list) or len(row) != k:
            return "matrix must have k columns"
        for c, v in enumerate(row):
            if v == 0:
                continue
            if not (1 <= v <= k) or v in pos:
                return "invalid or repeated value %r" % (v,)
            pos[v] = (r, c)
    if len(pos) != k:
        return "not every number 1..k appears"
    for a, b in rows:
        if not pos[a][0] < pos[b][0]:
            return "row condition violated: %d above %d" % (a, b)
    for a, b in cols:
        if not pos[a][1] < pos[b][1]:
            return "col condition violated: %d left of %d" % (a, b)
    return None


def make_dag(k, m, seed):
    rng = random.Random(seed)
    perm = list(range(1, k + 1))
    rng.shuffle(perm)
    edges = []
    for _ in range(m):
        i = rng.randrange(0, k - 1)
        j = rng.randrange(i + 1, k)
        edges.append([perm[i], perm[j]])
    # ensure a full chain so all nodes are constrained
    for i in range(k - 1):
        edges.append([perm[i], perm[i + 1]])
    return edges[:max(10000, k - 1)] if len(edges) > 10000 else edges


chain400 = [[i, i + 1] for i in range(1, 400)]
chain400_rev = [[i + 1, i] for i in range(1, 400)]

# (k, rowConditions, colConditions, feasible)
cases = [
    (3, [[1, 2], [3, 2]], [[2, 1], [3, 2]], True),
    (3, [[1, 2], [2, 3], [3, 1], [2, 3]], [[2, 1]], False),
    (2, [[1, 2]], [[1, 2]], True),
    (2, [[1, 2]], [[1, 2], [2, 1]], False),
    (2, [[2, 1], [1, 2]], [[1, 2]], False),
    (3, [[1, 2], [1, 2], [1, 2]], [[3, 1], [3, 1]], True),
    (4, [[1, 2]], [[3, 4]], True),
    (5, [[1, 2], [2, 3], [3, 4], [4, 5]], [[5, 4], [4, 3], [3, 2], [2, 1]], True),
    (4, [[1, 2]], [[2, 3], [3, 4], [4, 2]], False),
    (400, chain400, chain400_rev, True),
    (400, chain400 + [[400, 1]], chain400_rev, False),
    (400, make_dag(400, 4000, 7), make_dag(400, 4000, 11), True),
]

passed = 0
total = len(cases)
for n, (k, rc, cc, feasible) in enumerate(cases, 1):
    desc = "k=%d, rowConditions=%s, colConditions=%s" % (k, str(rc)[:80], str(cc)[:80])
    try:
        sol = ns["Solution"]()
        got = sol.buildMatrix(k, [list(x) for x in rc], [list(x) for x in cc])
        if feasible:
            err = validate(k, rc, cc, got)
            ok = err is None
            expected = "any valid matrix"
            if not ok:
                desc += " (%s)" % err
        else:
            ok = got == []
            expected = "[]"
        if ok:
            passed += 1
            print("PASS case %d" % n)
        else:
            shown = str(got)
            if len(shown) > 200:
                shown = shown[:200] + "..."
            print("FAIL case %d: input=%s, expected=%s, got=%s" % (n, desc, expected, shown))
    except Exception as e:
        print("FAIL case %d: input=%s, error=%s: %s" % (n, desc, type(e).__name__, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)
