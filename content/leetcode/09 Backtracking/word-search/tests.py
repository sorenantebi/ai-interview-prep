import sys
from collections import Counter, defaultdict, deque
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
    if not root:
        return []
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
    "Counter": Counter,
    "defaultdict": defaultdict,
    "deque": deque,
}
exec(open("attempt.py").read(), ns)

BIG = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]

all_a_6 = [["A"] * 6 for _ in range(6)]
one_b_6 = [["A"] * 6 for _ in range(6)]
one_b_6[5][5] = "B"

CASES = [
    (BIG, "ABCCED", True),
    (BIG, "SEE", True),
    (BIG, "ABCB", False),
    ([["A"]], "A", True),
    ([["A"]], "B", False),
    ([["A", "B"]], "ABA", False),
    ([["A", "B", "C"]], "CBA", True),
    ([["A"], ["B"], ["C"]], "ABC", True),
    ([["a", "B"]], "AB", False),
    ([["A", "A"], ["A", "A"]], "AAAAA", False),
    ([["A", "B", "C"], ["F", "E", "D"], ["G", "H", "I"]], "ABCDEFGHI", True),
    ([["A"] * 3 for _ in range(3)], "AAAAAAAAB", False),
    ([["C", "A", "A"], ["A", "A", "A"], ["B", "C", "D"]], "AAB", True),
    (all_a_6, "A" * 15, True),
    (one_b_6, "A" * 14 + "B", True),
]


def main():
    passed = 0
    total = len(CASES)
    for n, (board, word, expected) in enumerate(CASES, 1):
        desc = f"(board={board}, word={word!r})"
        try:
            sol = ns["Solution"]()
            got = sol.exist([row[:] for row in board], word)
            if bool(got) == expected and isinstance(got, bool):
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={desc}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input={desc}, error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()