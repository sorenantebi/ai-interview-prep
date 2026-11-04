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


def build_list(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = [root]
    i = 1
    while q and i < len(arr):
        n = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            n.left = TreeNode(arr[i])
            q.append(n.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            n.right = TreeNode(arr[i])
            q.append(n.right)
        i += 1
    return root


def tree_to_array(root):
    out = []
    q = [root]
    while q:
        n = q.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def close(a, b):
    return abs(a - b) <= 1e-5 * max(1.0, abs(b))


def lists_close(got, exp):
    if not isinstance(got, (list, tuple)) or len(got) != len(exp):
        return False
    return all(close(g, e) for g, e in zip(got, exp))


chain_eq = [["v%d" % i, "v%d" % (i + 1)] for i in range(20)]
chain_vals = [2.0] * 20

cases = [
    # 1: example 1
    ([["a", "b"], ["b", "c"]], [2.0, 3.0],
     [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]],
     [6.0, 0.5, -1.0, 1.0, -1.0]),
    # 2: example 2
    ([["a", "b"], ["b", "c"], ["bc", "cd"]], [1.5, 2.5, 5.0],
     [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]],
     [3.75, 0.4, 5.0, 0.2]),
    # 3: example 3
    ([["a", "b"]], [0.5],
     [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]],
     [0.5, 2.0, -1.0, -1.0]),
    # 4: self queries, defined vs undefined
    ([["a", "b"]], [2.0],
     [["a", "a"], ["b", "b"], ["c", "c"]],
     [1.0, 1.0, -1.0]),
    # 5: disconnected components
    ([["a", "b"], ["c", "d"]], [2.0, 3.0],
     [["a", "c"], ["c", "d"], ["d", "c"], ["b", "a"]],
     [-1.0, 3.0, 1.0 / 3.0, 0.5]),
    # 6: longest chain
    (chain_eq, chain_vals,
     [["v0", "v20"], ["v20", "v0"], ["v5", "v10"], ["v10", "v5"]],
     [1048576.0, 1.0 / 1048576.0, 32.0, 1.0 / 32.0]),
    # 7: consistent cycle
    ([["a", "b"], ["b", "c"], ["a", "c"]], [2.0, 3.0, 6.0],
     [["a", "c"], ["c", "a"], ["b", "c"]],
     [6.0, 1.0 / 6.0, 3.0]),
    # 8: star graph
    ([["a", "b"], ["a", "c"], ["a", "d"]], [2.0, 4.0, 8.0],
     [["b", "c"], ["c", "d"], ["d", "b"]],
     [2.0, 2.0, 0.25]),
    # 9: digit names and ratio 1
    ([["1", "2"]], [1.0],
     [["1", "2"], ["2", "1"], ["1", "3"]],
     [1.0, 1.0, -1.0]),
    # 10: undefined variable with defined one
    ([["a", "b"]], [20.0],
     [["a", "b"], ["b", "a"], ["z", "a"], ["a", "z"]],
     [20.0, 0.05, -1.0, -1.0]),
    # 11: fractional values over a chain
    ([["a", "b"], ["b", "c"], ["c", "d"]], [0.5, 0.2, 20.0],
     [["a", "d"], ["d", "a"], ["a", "c"], ["d", "b"]],
     [2.0, 0.5, 0.1, 0.25]),
    # 12: duplicated equation
    ([["a", "b"], ["a", "b"]], [2.0, 2.0],
     [["a", "b"], ["b", "a"]],
     [2.0, 0.5]),
]

passed = 0
total = len(cases)
for i, (eq, vals, qs, exp) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.calcEquation([list(e) for e in eq], list(vals), [list(q) for q in qs])
        if lists_close(got, exp):
            print("PASS case %d" % i)
            passed += 1
        else:
            print("FAIL case %d: input=%r, expected=%r, got=%r" % (i, (eq, vals, qs), exp, got))
    except Exception as e:
        print("FAIL case %d: input=%r, error=%s: %s" % (i, (eq, vals, qs), type(e).__name__, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)