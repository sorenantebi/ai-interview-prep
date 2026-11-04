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

CASES = [
    ([1, 2], 3, 1),
    ([3, 2, 2, 1], 3, 3),
    ([3, 5, 3, 4], 5, 4),
    ([1], 1, 1),
    ([5], 10, 1),
    ([2, 2, 2, 2], 4, 2),
    ([1, 1, 1, 1, 1], 2, 3),
    ([5, 5, 5], 5, 3),
    ([1, 2, 3, 4, 5], 6, 3),
    ([3, 1, 2, 3, 1, 2], 3, 4),
    ([1] * 25000 + [30000] * 25000, 30000, 37500),
    ([15000] * 50000, 30000, 25000),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


def main():
    passed = 0
    total = len(CASES)
    for n, (people, limit, expected) in enumerate(CASES, 1):
        arg = list(people)
        try:
            got = ns["Solution"]().numRescueBoats(arg, limit)
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input=({short(people)}, {limit}), expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input=({short(people)}, {limit}), error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()