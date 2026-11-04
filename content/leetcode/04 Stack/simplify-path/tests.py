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
    ("/home/", "/home"),
    ("/home//foo/", "/home/foo"),
    ("/home/user/Documents/../Pictures", "/home/user/Pictures"),
    ("/../", "/"),
    ("/.../a/../b/c/../d/./", "/.../b/d"),
    ("/", "/"),
    ("////", "/"),
    ("/a/./b/../../c/", "/c"),
    ("/a/../../b/../c//.//", "/c"),
    ("/a/b/c/../../../..", "/"),
    ("/..hidden/.../.a/a..", "/..hidden/.../.a/a.."),
    ("/_a1/B2/.", "/_a1/B2"),
    ("/a" * 750 + "/.." * 500, "/a" * 250),
]

passed = 0
total = len(cases)
for n, (path, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().simplifyPath(path)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            shown = path if len(path) <= 80 else path[:77] + "..."
            exp_s = expected if len(expected) <= 80 else expected[:77] + "..."
            got_s = got if not isinstance(got, str) or len(got) <= 80 else got[:77] + "..."
            print(f"FAIL case {n}: input={shown!r}, expected={exp_s!r}, got={got_s!r}")
    except Exception as e:
        shown = path if len(path) <= 80 else path[:77] + "..."
        print(f"FAIL case {n}: input={shown!r}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)