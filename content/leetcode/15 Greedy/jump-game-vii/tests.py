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
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out, q = [], [root]
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

N = 100000

# (s, minJump, maxJump, expected)
cases = [
    ("011010", 2, 3, True),
    ("01101110", 2, 3, False),
    ("00", 1, 1, True),
    ("01", 1, 1, False),
    ("0000", 1, 1, True),
    ("0100", 2, 2, False),
    ("00111110", 1, 5, False),
    ("00111110", 1, 6, True),
    ("0110", 1, 3, True),
    ("00000", 2, 2, True),
    ("000000", 2, 2, False),
    ("0111100", 3, 4, False),
    ("0" * (N - 1) + "1", 1, N // 2, False),
    ("0" * N, 1, 50000, True),
]

passed = 0
total = len(cases)
for idx, (s, lo, hi, expected) in enumerate(cases, 1):
    shown = s if len(s) <= 40 else f"<len {len(s)} string>"
    try:
        got = ns["Solution"]().canReach(s, lo, hi)
        if got == expected:
            passed += 1
            print(f"PASS case {idx}")
        else:
            print(f"FAIL case {idx}: input=({shown}, {lo}, {hi}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input=({shown}, {lo}, {hi}), expected={expected}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)