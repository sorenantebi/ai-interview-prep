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

# Every case has exactly one valid pair.
CASES = [
    (([2, 7, 11, 15], 9), [1, 2]),
    (([2, 3, 4], 6), [1, 3]),
    (([-1, 0], -1), [1, 2]),
    (([1, 1], 2), [1, 2]),
    (([0, 0, 3, 4], 0), [1, 2]),
    (([1, 2, 3, 4, 4, 9, 56, 90], 8), [4, 5]),
    (([-5, -3, -1, 0, 2, 8], -4), [2, 3]),
    (([-10, -4, 0, 3, 7, 20], -14), [1, 2]),
    (([1, 3, 5, 7, 9, 11], 20), [5, 6]),
    (([-1000, -500, 0, 500, 1000], -1000), [1, 3]),
    (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19), [9, 10]),
    (([0] * 29998 + [5, 7], 12), [29999, 30000]),
    (([3, 24, 50, 79, 88, 150, 345], 200), [3, 6]),
]


def main():
    passed = 0
    total = len(CASES)
    for n, (args, expected) in enumerate(CASES, 1):
        short = (args[0] if len(args[0]) <= 20 else f"<list of {len(args[0])}>", args[1])
        try:
            got = ns["Solution"]().twoSum(list(args[0]), args[1])
            got = list(got) if got is not None else got
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={short}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input={short}, expected={expected}, got=exception: {e!r}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()