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
    head = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
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


def tree_to_array(root):
    if not root:
        return []
    out, q = [], [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    ([3, 1, 2, 1], 5, [2, 1, 2, 1]),
    ([4, 1, 2, 2], 4, [3, 1, 2, 0]),
    ([7, 5, 5, 8, 3], 8, [6, 5, 0, 7, 5]),
    ([1], 1, [0]),
    ([1], 5, [0]),
    ([5], 5, [4]),
    ([1, 1, 1, 1], 3, [0, 0, 0, 0]),
    ([3, 2, 1], 3, [2, 2, 2]),
    ([2, 2, 3, 3, 1], 3, [1, 0, 2, 0, 2]),
    (list(range(1000, 0, -1)), 1000, [999] * 1000),
    (list(range(1, 1001)), 1000, list(range(0, 1000))),
    ([1000] * 1000, 1000, [999] + [0] * 999),
]

passed = 0
total = len(cases)
for idx, (queries, m, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().processQueries(list(queries), m)
        if list(got) == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            qs = queries if len(queries) <= 20 else f"<{len(queries)} items>"
            exp = expected if len(expected) <= 20 else f"<{len(expected)} items>"
            gt = got if got is None or len(got) <= 20 else f"<{len(got)} items>"
            print(f"FAIL case {idx}: input=(queries={qs}, m={m}), expected={exp}, got={gt}")
    except Exception as e:
        print(f"FAIL case {idx}: input=(m={m}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
