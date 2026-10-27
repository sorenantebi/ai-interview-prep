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


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
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


def run(nums, target):
    return ns["Solution"]().search(list(nums), target)


def rotate(arr, k):
    return arr[k:] + arr[:k]


big_sorted = list(range(-2500, 2500))
big_rot = rotate(big_sorted, 1234)

cases = [
    # examples
    ([4, 5, 6, 7, 0, 1, 2], 0, 4),
    ([4, 5, 6, 7, 0, 1, 2], 3, -1),
    ([1], 0, -1),
    # single element found
    ([1], 1, 0),
    # two elements
    ([3, 1], 1, 1),
    ([3, 1], 3, 0),
    # not rotated
    ([1, 2, 3, 4, 5], 4, 3),
    # rotated by n-1 (pivot at last)
    ([5, 1, 2, 3, 4], 5, 0),
    # negatives
    ([-3, -2, -1, -10, -8, -5], -10, 3),
    # target smaller than min / larger than max
    ([4, 5, 6, 7, 0, 1, 2], -1, -1),
    ([4, 5, 6, 7, 0, 1, 2], 8, -1),
    # large input
    (big_rot, big_sorted[4000], big_rot.index(big_sorted[4000])),
    (big_rot, 10000, -1),
]

passed = 0
total = len(cases)
for i, (nums, target, expected) in enumerate(cases, 1):
    try:
        got = run(nums, target)
        if got == expected:
            passed += 1
            print(f"PASS case {i}")
        else:
            shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
            print(f"FAIL case {i}: input=(nums={shown}, target={target}), expected={expected}, got={got}")
    except Exception as e:
        shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
        print(f"FAIL case {i}: input=(nums={shown}, target={target}), expected={expected}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)