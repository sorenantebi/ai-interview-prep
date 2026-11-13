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
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = [root]
    i = 1
    while q and i < len(arr):
        n = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            n.left = TreeNode(arr[i])
            q.append(n.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            n.right = TreeNode(arr[i])
            q.append(n.right)
        i += 1
    return root


def tree_to_array(root):
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
    ("3+2*2", 7),
    (" 3/2 ", 1),
    (" 3+5 / 2 ", 5),
    ("42", 42),
    ("0", 0),
    ("1-1+1", 1),
    ("14-3/2", 13),
    ("100000000/1000/10/10", 1000),
    ("2*3*4/5", 4),
    ("0-5/2", -2),
    ("0-7/2", -3),
    ("2147483647*1/1", 2147483647),
    ("  12  *  3  -  4  /  2  ", 34),
    ("1" + "+1" * 149999, 150000),
    ("1+" * 100000 + "1 ", 100001),
]

passed = 0
total = len(cases)
for idx, (s, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.calculate(s)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            shown = s if len(s) <= 60 else s[:60] + "..."
            print(f"FAIL case {idx}: input={shown!r}, expected={expected}, got={got}")
    except Exception as e:
        shown = s if len(s) <= 60 else s[:60] + "..."
        print(f"FAIL case {idx}: input={shown!r}, expected={expected}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
