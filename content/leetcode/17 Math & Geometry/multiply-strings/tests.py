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


def run(num1, num2):
    return ns["Solution"]().multiply(num1, num2)


big_a = "9" * 200
big_b = "9" * 200
big_c = "123456789" * 22 + "12"
big_d = "987654321" * 22 + "98"

cases = [
    ("2", "3", "6"),
    ("123", "456", "56088"),
    ("0", "52", "0"),
    ("52", "0", "0"),
    ("0", "0", "0"),
    ("1", "1", "1"),
    ("9", "9", "81"),
    ("99", "99", "9801"),
    ("100", "100", "10000"),
    ("999", "1", "999"),
    ("12345", "6789", str(12345 * 6789)),
    (big_a, big_b, str(int(big_a) * int(big_b))),
    (big_c, big_d, str(int(big_c) * int(big_d))),
    ("1" + "0" * 199, "1" + "0" * 199, "1" + "0" * 398),
]

passed = 0
total = len(cases)
for n, (a, b, expected) in enumerate(cases, 1):
    try:
        got = run(a, b)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input=({a!r}, {b!r}), expected={expected!r}, got={got!r}")
    except Exception as e:
        print(f"FAIL case {n}: input=({a!r}, {b!r}), expected={expected!r}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)