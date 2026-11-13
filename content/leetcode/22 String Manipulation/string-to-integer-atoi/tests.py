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


def list_to_arr(node):
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
        node = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_arr(root):
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

CASES = [
    ("42", 42),
    (" -042", -42),
    ("1337c0d3", 1337),
    ("0-1", 0),
    ("words and 987", 0),
    ("", 0),
    ("   ", 0),
    ("-", 0),
    ("+-12", 0),
    ("+1", 1),
    ("3.14159", 3),
    ("   +0 123", 0),
    ("0000000000012345678", 12345678),
    ("2147483647", 2147483647),
    ("-2147483648", -2147483648),
    ("2147483648", 2147483647),
    ("-91283472332", -2147483648),
    ("9" * 200, 2147483647),
    ("-" + "9" * 199, -2147483648),
]


def main():
    passed = 0
    total = len(CASES)
    for idx, (s, expected) in enumerate(CASES, 1):
        try:
            got = ns["Solution"]().myAtoi(s)
            if got == expected and not isinstance(got, bool):
                print(f"PASS case {idx}")
                passed += 1
            else:
                print(f"FAIL case {idx}: input={s!r}, expected={expected!r}, got={got!r}")
        except Exception as e:
            print(f"FAIL case {idx}: input={s!r}, expected={expected!r}, got=exception {type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()