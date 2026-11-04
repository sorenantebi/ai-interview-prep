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
    head = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = [root]
    i = 1
    while q and i < len(arr):
        node = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    # (nums, k, expected)
    ([4, 2, 1, 4, 3, 4, 5, 8, 15], 3, 5),
    ([7, 4, 5, 1, 8, 12, 4, 7], 5, 4),
    ([1, 5], 1, 1),
    ([1], 1, 1),
    ([5, 5, 5, 5], 3, 1),
    ([1, 2, 3, 4, 5], 1, 5),
    ([5, 4, 3, 2, 1], 100000, 1),
    ([1, 100000], 100000, 2),
    ([1, 3, 5, 7, 9], 1, 1),
    ([1, 3, 5, 7, 9], 2, 5),
    ([1, 2, 4, 3], 2, 3),
    ([1, 10, 2, 11, 3, 12], 2, 3),
    (list(range(1, 100001)), 1, 100000),
    (list(range(1, 50001)) * 2, 1, 50000),
]

passed = 0
total = len(cases)
for i, (nums, k, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 20 else f"<list of {len(nums)} elements>"
    try:
        sol = ns["Solution"]()
        got = sol.lengthOfLIS(list(nums), k)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=(nums={shown}, k={k}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input=(nums={shown}, k={k}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)