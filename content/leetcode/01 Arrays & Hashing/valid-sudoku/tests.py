import sys
import collections
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


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


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
    queue = collections.deque([root])
    i = 1
    while queue and i < len(vals):
        node = queue.popleft()
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
    queue = collections.deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
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


def make(rows):
    return [list(r) for r in rows]


def empty():
    return make(["........."] * 9)


def with_cells(cells):
    b = empty()
    for (r, c), d in cells.items():
        b[r][c] = d
    return b


EXAMPLE = make([
    "53..7....",
    "6..195...",
    ".98....6.",
    "8...6...3",
    "4..8.3..1",
    "7...2...6",
    ".6....28.",
    "...419..5",
    "....8..79",
])

EXAMPLE_BAD = copy.deepcopy(EXAMPLE)
EXAMPLE_BAD[0][0] = "8"

SOLVED = make([
    "534678912",
    "672195348",
    "198342567",
    "859761423",
    "426853791",
    "713924856",
    "961537284",
    "287419635",
    "345286179",
])

ones = {(0, 0): "1", (1, 3): "1", (2, 6): "1", (3, 1): "1", (4, 4): "1",
        (5, 7): "1", (6, 2): "1", (7, 5): "1", (8, 8): "1"}

cases = [
    (EXAMPLE, True),                                        # example 1
    (EXAMPLE_BAD, False),                                   # example 2
    (empty(), True),                                        # empty board
    (with_cells({(4, 4): "9"}), True),                      # single cell
    (SOLVED, True),                                         # full valid board
    (with_cells(ones), True),                               # same digit, no conflicts
    (with_cells({(0, 0): "5", (0, 3): "5"}), False),        # row dup, different boxes
    (with_cells({(0, 0): "7", (3, 0): "7"}), False),        # column dup, different boxes
    (with_cells({(0, 0): "3", (1, 1): "3"}), False),        # box dup only
    (with_cells({(3, 3): "4", (5, 5): "4"}), False),        # center box dup only
    (with_cells({(6, 6): "2", (8, 8): "2"}), False),        # last box dup
    (with_cells({(8, 0): "9", (8, 8): "9"}), False),        # row dup at far ends
    (with_cells({(0, 8): "6", (8, 8): "6"}), False),        # column dup at far ends
]

passed = 0
total = len(cases)
for n, (board, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().isValidSudoku(copy.deepcopy(board))
        if got is expected or got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            print(f"FAIL case {n}: input={board}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={board}, expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)