import copy
import re
import sys
from collections import deque
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
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    out = []
    q = deque([root])
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
    "deque": deque,
}

src = open("attempt.py").read()
try:
    exec(compile(src, "attempt.py", "exec"), ns)
except SyntaxError:
    # Fall back to loading top-level chunks (class/def blocks) independently,
    # skipping any chunk that does not compile.
    lines = src.split("\n")
    chunks, cur = [], []
    for line in lines:
        if re.match(r"(class |def )", line) and cur:
            chunks.append("\n".join(cur))
            cur = []
        cur.append(line)
    if cur:
        chunks.append("\n".join(cur))
    for chunk in chunks:
        try:
            exec(compile(chunk, "attempt.py", "exec"), ns)
        except SyntaxError:
            continue


def to_grid(rows):
    return [list(r) for r in rows]


cases = [
    # examples
    (to_grid(["11110", "11010", "11000", "00000"]), 1),
    (to_grid(["11000", "11000", "00100", "00011"]), 3),
    # single cells
    (to_grid(["1"]), 1),
    (to_grid(["0"]), 0),
    # all water / all land
    (to_grid(["000", "000", "000"]), 0),
    (to_grid(["111", "111", "111"]), 1),
    # diagonals are not connected
    (to_grid(["101", "010", "101"]), 5),
    (to_grid(["10", "01"]), 2),
    # single row / single column
    (to_grid(["1011011"]), 3),
    (to_grid(["1", "0", "1", "1", "0", "1"]), 3),
    # snake shape (one island, winding)
    (to_grid(["11111", "00001", "11111", "10000", "11111"]), 1),
    # island touching borders and enclosing a lake
    (to_grid(["111", "101", "111"]), 1),
    # large: checkerboard 300x300 -> 45000 single-cell islands
    ([["1" if (r + c) % 2 == 0 else "0" for c in range(300)] for r in range(300)], 45000),
    # large: alternating land/water rows 300x300 -> 150 islands
    ([["1" if r % 2 == 0 else "0" for c in range(300)] for r in range(300)], 150),
]

passed = 0
total = len(cases)
for i, (grid, expected) in enumerate(cases, 1):
    desc = grid if len(grid) * len(grid[0]) <= 50 else f"<{len(grid)}x{len(grid[0])} grid>"
    try:
        got = ns["Solution"]().numIslands(copy.deepcopy(grid))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={desc}, expected={expected}, got={got}")
    except BaseException as e:
        print(f"FAIL case {i}: input={desc}, expected={expected}, got={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)