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
    ([[1993, 1999], [2000, 2010]], 1993),
    ([[1950, 1961], [1960, 1971], [1970, 1981]], 1960),
    ([[1950, 2050]], 1950),
    ([[2049, 2050]], 2049),
    ([[1950, 1951], [1951, 1952]], 1950),
    ([[2000, 2005]] * 3, 2000),
    ([[1960, 1970], [1970, 1980]], 1960),
    ([[1950, 1955], [1990, 2000], [1995, 2005]], 1995),
    ([[1955, 1965], [1960, 1970], [1950, 1961]], 1960),
    ([[1950 + i, 1951 + i] for i in range(100)], 1950),
    ([[1950 + i, 2050 - i] for i in range(50)], 1999),
    ([[2000, 2001]] * 100, 2000),
]

passed = 0
total = len(cases)
for n, (logs, expected) in enumerate(cases, 1):
    try:
        inp = [list(x) for x in logs]
        got = ns["Solution"]().maximumPopulation(inp)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={logs}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={logs}, expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
