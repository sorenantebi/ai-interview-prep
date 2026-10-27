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


def expected_plus_one(digits):
    n = int("".join(map(str, digits))) + 1
    return [int(c) for c in str(n)]


cases = [
    [1, 2, 3],
    [4, 3, 2, 1],
    [9],
    [0],
    [8],
    [1, 9],
    [9, 9],
    [9, 9, 9, 9],
    [1, 0, 0],
    [1, 2, 9, 9],
    [9, 8, 9],
    [5, 0, 9, 9, 9, 9, 9, 9],
    [9] * 100,
    [1] + [9] * 99,
    [7] * 100,
]

explicit = {
    0: [1, 2, 4],
    1: [4, 3, 2, 2],
    2: [1, 0],
}

passed = 0
total = len(cases)
for idx, digits in enumerate(cases, 1):
    expected = explicit.get(idx - 1, expected_plus_one(digits))
    arg = list(digits)
    try:
        sol = ns["Solution"]()
        got = sol.plusOne(arg)
        got = list(got) if got is not None else got
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={digits}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={digits}, expected={expected}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
