import sys
from collections import deque
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


def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def serialize_tree(root):
    if root is None:
        return []
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def serialize_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def chain(n, side="left", start=1):
    """Build a degenerate tree of n nodes as a level-order list."""
    root = TreeNode(start)
    cur = root
    for k in range(1, n):
        node = TreeNode(start + k)
        setattr(cur, side, node)
        cur = node
    return root


def full_tree_values(n):
    return list(range(n))


cases = [
    # (p_values, q_values, expected)
    ([1, 2, 3], [1, 2, 3], True),
    ([1, 2], [1, None, 2], False),
    ([1, 2, 1], [1, 1, 2], False),
    ([], [], True),
    ([], [1], False),
    ([1], [], False),
    ([1], [1], True),
    ([1], [2], False),
    ([-5, -10, 10000], [-5, -10, 10000], True),
    ([-5, -10, 10000], [-5, -10, -10000], False),
    ([1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, None], False),
    ([1, 2, 3, None, 4, 5, None], [1, 2, 3, None, 4, 5, None], True),
]

# Large-input cases built directly (deep chains and a full tree)
large_cases = [
    ("chain of 100 left, identical", chain(100, "left"), chain(100, "left"), True),
    ("chain of 100 left vs right", chain(100, "left"), chain(100, "right"), False),
    ("full tree of 100, identical", build_tree(full_tree_values(100)), build_tree(full_tree_values(100)), True),
]

total = 0
passed = 0


def run_case(label, p, q, expected, shown):
    global total, passed
    total += 1
    try:
        sol = ns["Solution"]()
        got = sol.isSameTree(p, q)
        ok = (got is expected) or (isinstance(got, bool) and got == expected)
        if ok:
            passed += 1
            print(f"PASS case {total}")
        else:
            print(f"FAIL case {total}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {total}: input={shown}, expected={expected}, got=error: {type(e).__name__}: {e}")


for pv, qv, exp in cases:
    run_case(None, build_tree(pv), build_tree(qv), exp, f"p={pv}, q={qv}")

for name, p, q, exp in large_cases:
    run_case(name, p, q, exp, name)

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)