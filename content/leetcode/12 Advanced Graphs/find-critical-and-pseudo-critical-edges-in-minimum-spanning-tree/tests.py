import sys
import copy
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
    out = []
    q = [root]
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


def norm(res):
    return [sorted(res[0]), sorted(res[1])]


big_path = [[i, i + 1, 1 + (i % 10)] for i in range(99)]
big_path += [[i, i + 2, 1000] for i in range(98)]

big_cycle = [[i, i + 1, 1] for i in range(99)] + [[0, 99, 1]]

cases = [
    (5, [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]],
     [[0, 1], [2, 3, 4, 5]]),
    (4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]], [[], [0, 1, 2, 3]]),
    (2, [[0, 1, 5]], [[0], []]),
    (4, [[0, 1, 1], [1, 2, 2], [2, 3, 3]], [[0, 1, 2], []]),
    (3, [[0, 1, 1], [1, 2, 2], [0, 2, 3]], [[0, 1], []]),
    (3, [[0, 1, 1], [1, 2, 1], [0, 2, 2]], [[0, 1], []]),
    (3, [[0, 1, 5], [1, 2, 5], [0, 2, 5]], [[], [0, 1, 2]]),
    (4, [[0, 1, 1], [0, 2, 1], [1, 2, 1], [2, 3, 4]], [[3], [0, 1, 2]]),
    (4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 5], [0, 2, 5]], [[0, 1, 2], []]),
    (5, [[0, 1, 1], [1, 2, 1], [0, 2, 1], [2, 3, 2], [3, 4, 2], [2, 4, 2]],
     [[], [0, 1, 2, 3, 4, 5]]),
    (4, [[2, 3, 7], [0, 1, 1], [1, 2, 1], [0, 2, 1]], [[0], [1, 2, 3]]),
    (100, big_path, [list(range(99)), []]),
    (100, big_cycle, [[], list(range(100))]),
]

passed = 0
total = len(cases)
for idx, (n, edges, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.findCriticalAndPseudoCriticalEdges(n, copy.deepcopy(edges))
        if norm(got) == norm(expected):
            print(f"PASS case {idx}")
            passed += 1
        else:
            shown = edges if len(edges) <= 20 else f"<{len(edges)} edges>"
            print(f"FAIL case {idx}: input=n={n}, edges={shown}, expected={norm(expected) if len(edges) <= 20 else '<large>'}, got={norm(got) if len(edges) <= 20 else '<large>'}")
    except Exception as e:
        print(f"FAIL case {idx}: input=n={n}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
