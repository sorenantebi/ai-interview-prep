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
    if not root:
        return []
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
    (123, "One Hundred Twenty Three"),
    (12345, "Twelve Thousand Three Hundred Forty Five"),
    (1234567, "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"),
    (0, "Zero"),
    (1, "One"),
    (10, "Ten"),
    (19, "Nineteen"),
    (20, "Twenty"),
    (100, "One Hundred"),
    (101, "One Hundred One"),
    (1000, "One Thousand"),
    (100000, "One Hundred Thousand"),
    (1000010, "One Million Ten"),
    (1000000000, "One Billion"),
    (2147483647, "Two Billion One Hundred Forty Seven Million Four Hundred Eighty Three Thousand Six Hundred Forty Seven"),
]


def main():
    passed = 0
    total = len(CASES)
    for i, (num, expected) in enumerate(CASES, 1):
        try:
            got = ns["Solution"]().numberToWords(num)
            if got == expected:
                print(f"PASS case {i}")
                passed += 1
            else:
                print(f"FAIL case {i}: input={num!r}, expected={expected!r}, got={got!r}")
        except Exception as e:
            print(f"FAIL case {i}: input={num!r}, expected={expected!r}, got=Exception: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()
