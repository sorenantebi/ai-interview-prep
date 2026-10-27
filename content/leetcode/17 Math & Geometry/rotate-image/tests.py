import sys
import copy
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


def expected_rotate(m):
    n = len(m)
    return [[m[n - 1 - j][i] for j in range(n)] for i in range(n)]


def make_cases():
    cases = []
    cases.append([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    cases.append([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]])
    cases.append([[1]])
    cases.append([[1, 2], [3, 4]])
    cases.append([[-1, -2], [-3, -4]])
    cases.append([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    cases.append([[7, 7], [7, 7]])
    cases.append([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15],
                  [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]])
    cases.append([[-1000, 1000], [0, -1]])
    rnd = random.Random(42)
    cases.append([[rnd.randint(-1000, 1000) for _ in range(6)] for _ in range(6)])
    cases.append([[rnd.randint(-1000, 1000) for _ in range(19)] for _ in range(19)])
    cases.append([[rnd.randint(-1000, 1000) for _ in range(20)] for _ in range(20)])
    return cases


def run_case(m):
    sol = ns["Solution"]()
    mat = copy.deepcopy(m)
    ident = id(mat)
    row_ids = [id(r) for r in mat]
    ret = sol.rotate(mat)
    exp = expected_rotate(m)
    if ret is not None:
        return False, exp, mat, "returned %r instead of None" % (ret,)
    if id(mat) != ident or [id(r) for r in mat] != row_ids:
        # rows replaced by new lists: not truly in place
        if mat != exp:
            return False, exp, mat, ""
        return False, exp, mat, "row objects were replaced (not in place)"
    return mat == exp, exp, mat, ""


def main():
    cases = make_cases()
    passed = 0
    for i, m in enumerate(cases, 1):
        try:
            ok, exp, got, note = run_case(m)
        except Exception as e:
            print("FAIL case %d: input=%r, error=%s: %s" % (i, m, type(e).__name__, e))
            continue
        if ok:
            passed += 1
            print("PASS case %d" % i)
        else:
            extra = (", note=" + note) if note else ""
            print("FAIL case %d: input=%r, expected=%r, got=%r%s" % (i, m, exp, got, extra))
    print("%d/%d passed" % (passed, len(cases)))
    if passed != len(cases):
        sys.exit(1)


main()
