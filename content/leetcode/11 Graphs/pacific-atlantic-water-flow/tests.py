import sys
import random
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
        n = q.popleft()
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


def oracle(heights):
    # iterative reverse BFS, no recursion
    R, C = len(heights), len(heights[0])

    def bfs(starts):
        seen = set(starts)
        q = deque(starts)
        while q:
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen \
                        and heights[nr][nc] >= heights[r][c]:
                    seen.add((nr, nc))
                    q.append((nr, nc))
        return seen

    pac = bfs([(0, c) for c in range(C)] + [(r, 0) for r in range(R)])
    atl = bfs([(R - 1, c) for c in range(C)] + [(r, C - 1) for r in range(R)])
    return sorted([r, c] for r, c in pac & atl)


def canon(res):
    return sorted([list(x) for x in res])


random.seed(12345)

ex1 = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
rand_small = [[random.randint(0, 9) for _ in range(6)] for _ in range(5)]
rand_big = [[random.randint(0, 10**5) for _ in range(200)] for _ in range(200)]
diag_big = [[r + c for c in range(200)] for r in range(200)]

cases = [
    (ex1, [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]),
    ([[1]], [[0, 0]]),
    ([[1, 2, 3]], [[0, 0], [0, 1], [0, 2]]),
    ([[3], [1], [2]], [[0, 0], [1, 0], [2, 0]]),
    ([[5, 5, 5], [5, 5, 5], [5, 5, 5]], [[r, c] for r in range(3) for c in range(3)]),
    ([[1, 2], [4, 3]], [[0, 1], [1, 0], [1, 1]]),
    ([[0, 0], [0, 0]], [[0, 0], [0, 1], [1, 0], [1, 1]]),
    (rand_small, oracle(rand_small)),
    ([[10, 1, 10], [1, 1, 1], [10, 1, 10]], oracle([[10, 1, 10], [1, 1, 1], [10, 1, 10]])),
    ([[r * 4 + c for c in range(4)] for r in range(4)], oracle([[r * 4 + c for c in range(4)] for r in range(4)])),
    (rand_big, oracle(rand_big)),
    (diag_big, oracle(diag_big)),
]

passed = 0
total = len(cases)
for i, (heights, expected) in enumerate(cases, 1):
    desc = "<%dx%d grid>" % (len(heights), len(heights[0])) if len(heights) * len(heights[0]) > 50 else repr(heights)
    try:
        inp = [row[:] for row in heights]
        got = ns["Solution"]().pacificAtlantic(inp)
        if canon(got) == canon(expected):
            print("PASS case %d" % i)
            passed += 1
        else:
            if len(expected) > 30:
                print("FAIL case %d: input=%s, expected=%d cells, got=%d cells" % (i, desc, len(expected), len(got)))
            else:
                print("FAIL case %d: input=%s, expected=%s, got=%s" % (i, desc, canon(expected), canon(got)))
    except BaseException as e:
        print("FAIL case %d: input=%s, error=%s: %s" % (i, desc, type(e).__name__, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)