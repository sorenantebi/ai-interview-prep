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


def reference(s):
    prev2, prev1 = 0, 1
    for i in range(1, len(s) + 1):
        cur = 0
        if s[i - 1] != "0":
            cur += prev1
        if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    ("12", 2),
    ("226", 3),
    ("06", 0),
    ("0", 0),
    ("1", 1),
    ("10", 1),
    ("27", 1),
    ("100", 0),
    ("2101", 1),
    ("11106", 2),
    ("2611055971756562", 4),
    ("301", 0),
    ("1" * 45, reference("1" * 45)),
    ("10" * 50, 1),
    ("27" * 50, 1),
]


def main():
    passed = 0
    total = len(cases)
    for n, (s, expected) in enumerate(cases, 1):
        try:
            got = ns["Solution"]().numDecodings(s)
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={s!r}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input={s!r}, expected={expected}, got=error: {type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()