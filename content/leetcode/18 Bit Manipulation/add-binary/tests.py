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
    ("11", "1", "100"),
    ("1010", "1011", "10101"),
    ("0", "0", "0"),
    ("0", "1", "1"),
    ("1", "0", "1"),
    ("1", "1", "10"),
    ("1111", "1", "10000"),
    ("101", "1", "110"),
    ("1", "111000", "111001"),
    ("0", "1010", "1010"),
    ("100000", "1", "100001"),
    ("1" * 10000, "1", "1" + "0" * 10000),
    ("1" * 10000, "1" * 10000, "1" * 10000 + "0"),
]

passed = 0
total = len(cases)
for n, (a, b, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().addBinary(a, b)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            sa = a if len(a) <= 40 else a[:20] + "...(" + str(len(a)) + " chars)"
            sb = b if len(b) <= 40 else b[:20] + "...(" + str(len(b)) + " chars)"
            se = expected if len(expected) <= 40 else expected[:20] + "...(" + str(len(expected)) + " chars)"
            sg = got if not isinstance(got, str) or len(got) <= 40 else got[:20] + "...(" + str(len(got)) + " chars)"
            print(f"FAIL case {n}: input=a={sa!r}, b={sb!r}, expected={se!r}, got={sg!r}")
    except Exception as e:
        print(f"FAIL case {n}: input=a={a[:40]!r}, b={b[:40]!r}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
