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
    queue = [root]
    i = 1
    while queue and i < len(arr):
        node = queue.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
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
    ("aba", True),
    ("abca", True),
    ("abc", False),
    ("a", True),
    ("aa", True),
    ("ab", True),
    ("abcba", True),
    ("deeee", True),
    ("eccer", True),
    ("abcdefa", False),
    ("abbca", True),
    ("abcddcbea", True),
    ("cbbcc", True),
    ("a" * 100000, True),
    ("a" * 50000 + "bcd" + "a" * 50000, False),
]


def show(s):
    return repr(s) if len(s) <= 50 else "<str len=%d>" % len(s)


passed = 0
total = len(cases)
for n, (s, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().validPalindrome(s)
        if got == expected:
            print("PASS case %d" % n)
            passed += 1
        else:
            print("FAIL case %d: input=%s, expected=%s, got=%s" % (n, show(s), expected, got))
    except Exception as e:
        print("FAIL case %d: input=%s, expected=%s, got=error: %s" % (n, show(s), expected, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)
