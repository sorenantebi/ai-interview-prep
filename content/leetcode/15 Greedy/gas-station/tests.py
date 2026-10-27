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
    qi = 0
    while qi < len(queue) and i < len(vals):
        node = queue[qi]
        qi += 1
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
    qi = 0
    while qi < len(queue):
        node = queue[qi]
        qi += 1
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


def is_valid_start(gas, cost, s):
    n = len(gas)
    if not isinstance(s, int) or isinstance(s, bool) or s < 0 or s >= n:
        return False
    tank = 0
    for k in range(n):
        i = (s + k) % n
        tank += gas[i] - cost[i]
        if tank < 0:
            return False
    return True


def short(x, limit=80):
    s = str(x)
    return s if len(s) <= limit else s[:limit] + "..."


# (gas, cost, expected); expected == -1 means infeasible, otherwise got must be a valid
# starting station (equal to expected whenever the solution is unique).
cases = [
    ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3),
    ([2, 3, 4], [3, 4, 3], -1),
    ([5], [4], 0),
    ([4], [5], -1),
    ([0], [0], 0),
    ([3, 1, 1], [1, 2, 2], 0),
    ([1, 2, 3], [2, 3, 1], 2),
    ([5, 1, 2, 3, 4], [4, 4, 1, 5, 1], 4),
    ([3, 3, 4], [3, 4, 4], -1),
    ([0, 0, 0], [0, 0, 0], 0),
    ([0] * 50000 + [1] * 50000, [1] * 50000 + [0] * 50000, 50000),
    ([10000] * 100000, [10000] * 99999 + [10001], -1),
]

passed = 0
total = len(cases)
for idx, (gas, cost, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.canCompleteCircuit(list(gas), list(cost))
        if expected == -1:
            ok = got == -1
        else:
            ok = is_valid_start(gas, cost, got)
        if ok:
            passed += 1
            print(f"PASS case {idx}")
        else:
            print(f"FAIL case {idx}: input=gas={short(gas)}, cost={short(cost)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input=gas={short(gas)}, cost={short(cost)}, expected={expected}, got=exception {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)