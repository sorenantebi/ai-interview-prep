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
    ([7, 1, 5, 3, 6, 4], 7),
    ([1, 2, 3, 4, 5], 4),
    ([7, 6, 4, 3, 1], 0),
    ([5], 0),
    ([3, 3, 3, 3], 0),
    ([1, 2], 1),
    ([2, 1], 0),
    ([1, 5, 1, 5, 1, 5], 12),
    ([0, 10000], 10000),
    ([1, 3, 2, 4, 3, 5], 6),
    ([6, 1, 3, 2, 4, 7], 7),
    ([0, 10000] * 15000, 150000000),
    (list(range(0, 10001)), 10000),
]


def main():
    passed = 0
    total = len(CASES)
    for n, (prices, expected) in enumerate(CASES, 1):
        shown = prices if len(prices) <= 20 else f"<list of {len(prices)} items>"
        try:
            got = ns["Solution"]().maxProfit(list(prices))
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={shown}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input={shown}, expected={expected}, got=exception: {e!r}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()