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
    (11, 3),
    (128, 1),
    (2147483645, 30),
    (1, 1),
    (2, 1),
    (3, 2),
    (2**31 - 1, 31),
    (2**30, 1),
    (2**32 - 1, 32),
    (0b10101010101010101010101010101010, 16),
    (1023, 10),
    (1024, 1),
    (2**31 - 2, 30),
    (100000, bin(100000).count("1")),
]

passed = 0
total = len(cases)
for idx, (n, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().hammingWeight(n)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={n}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={n}, expected={expected}, got=exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
