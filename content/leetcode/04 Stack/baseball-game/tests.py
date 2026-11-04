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


def list_to_py(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = [root]
    i = 1
    while q and i < len(vals):
        n = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i])
            q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i])
            q.append(n.right)
        i += 1
    return root


def tree_to_list(root):
    out = []
    q = [root]
    while q:
        n = q.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    (["5", "2", "C", "D", "+"], 30),
    (["5", "-2", "4", "C", "D", "9", "+", "+"], 27),
    (["1", "C"], 0),
    (["7"], 7),
    (["-5", "D"], -15),
    (["3", "D", "D", "D"], 45),
    (["1", "2", "+", "+", "+"], 19),
    (["10", "C", "20", "C", "30"], 30),
    (["0", "D", "+"], 0),
    (["30000", "30000", "+", "D"], 240000),
    (["-1", "-2", "+", "C", "C", "D"], -3),
    (["5", "D", "C"] * 333 + ["7"], 1672),
]

passed = 0
total = len(cases)
for i, (ops, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().calPoints(list(ops))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            shown = ops if len(ops) <= 20 else f"<{len(ops)} ops>"
            print(f"FAIL case {i}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        shown = ops if len(ops) <= 20 else f"<{len(ops)} ops>"
        print(f"FAIL case {i}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)