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

cases = [
    ([5, 2, 6, 1], [2, 1, 1, 0]),
    ([-1], [0]),
    ([-1, -1], [0, 0]),
    ([1, 2, 3], [0, 0, 0]),
    ([3, 2, 1], [2, 1, 0]),
    ([2, 0, 1], [2, 0, 0]),
    ([1, 1, 1, 1], [0, 0, 0, 0]),
    ([-10000, 10000, -10000, 10000], [0, 1, 0, 0]),
    ([0, -1, -2, -3, 0], [3, 2, 1, 0, 0]),
    (list(range(10000, -10001, -1)), list(range(20000, -1, -1))),
    ([-10000 + (i * 20001) // 100000 for i in range(100000)], [0] * 100000),
]

passed = 0
total = len(cases)
for n, (nums, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
    try:
        got = ns["Solution"]().countSmaller(list(nums))
        if list(got) == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            exp_s = expected if len(expected) <= 20 else f"<list of {len(expected)}>"
            got_s = got if len(got) <= 20 else f"<list of {len(got)}>"
            print(f"FAIL case {n}: input={shown}, expected={exp_s}, got={got_s}")
    except Exception as e:
        print(f"FAIL case {n}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
