import sys
import copy
import collections
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
    q = collections.deque([root])
    i = 1
    while q and i < len(arr):
        node = q.popleft()
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
    q = collections.deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "collections": collections,
}
exec(open("attempt.py").read(), ns)


def reference(grid):
    grid = copy.deepcopy(grid)
    q = collections.deque()
    fresh = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1:
                fresh += 1
            elif grid[r][c] == 2:
                q.append((r, c))
    t = 0
    while fresh > 0 and q:
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    q.append((nr, nc))
                    fresh -= 1
        t += 1
    return t if fresh == 0 else -1


big_snake = [[1] * 10 for _ in range(10)]
big_snake[0][0] = 2

cases = [
    ([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4),
    ([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1),
    ([[0, 2]], 0),
    ([[0]], 0),
    ([[1]], -1),
    ([[2]], 0),
    ([[1, 2]], 1),
    ([[2, 1, 1, 1, 1]], 4),
    ([[2], [1], [1], [1]], 3),
    ([[2, 1, 2], [1, 1, 1], [2, 1, 2]], 2),
    ([[0, 0], [0, 0]], 0),
    ([[2, 0, 1]], -1),
    (big_snake, 18),
    ([[2 if (r + c) % 7 == 0 else (0 if (r * c) % 5 == 4 else 1) for c in range(10)] for r in range(10)], None),
]

passed = 0
total = len(cases)
for i, (grid, expected) in enumerate(cases, 1):
    if expected is None:
        expected = reference(grid)
    inp = copy.deepcopy(grid)
    try:
        sol = ns["Solution"]()
        got = sol.orangesRotting(copy.deepcopy(grid))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={inp}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={inp}, expected={expected}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)