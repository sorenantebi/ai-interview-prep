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
    ("III", 3),
    ("LVIII", 58),
    ("MCMXCIV", 1994),
    ("I", 1),
    ("IV", 4),
    ("IX", 9),
    ("XL", 40),
    ("XC", 90),
    ("CD", 400),
    ("CM", 900),
    ("XLIX", 49),
    ("MCDXLIV", 1444),
    ("MDCLXVI", 1666),
    ("MMMDCCCLXXXVIII", 3888),
    ("MMMCMXCIX", 3999),
]

passed = 0
total = len(CASES)
for n, (s, expected) in enumerate(CASES, 1):
    try:
        got = ns["Solution"]().romanToInt(s)
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            print(f"FAIL case {n}: input={s!r}, expected={expected!r}, got={got!r}")
    except Exception as e:
        print(f"FAIL case {n}: input={s!r}, expected={expected!r}, got=exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)