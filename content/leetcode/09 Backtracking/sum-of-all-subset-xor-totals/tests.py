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

CASES = [
    ([1, 3], 6),
    ([5, 1, 6], 28),
    ([3, 4, 5, 6, 7, 8], 480),
    ([1], 1),
    ([20], 20),
    ([1, 1], 2),
    ([2, 2, 2], 8),
    ([1, 2, 4, 8, 16], 496),
    ([20] * 12, 40960),
    (list(range(1, 13)), 30720),
    ([20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9], 63488),
    ([16, 1], 34),
    ([7, 7, 7, 7], 56),
]


def main():
    passed = 0
    total = len(CASES)
    for i, (nums, expected) in enumerate(CASES, 1):
        try:
            got = ns["Solution"]().subsetXORSum(list(nums))
            if got == expected:
                print(f"PASS case {i}")
                passed += 1
            else:
                print(f"FAIL case {i}: input={nums}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {i}: input={nums}, expected={expected}, got=error: {e!r}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()