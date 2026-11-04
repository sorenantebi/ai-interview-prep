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

N_BIG = 100000
big1 = [[3, i, i + 1] for i in range(1, N_BIG)] + [[1, 1, N_BIG]]

N_MID = 50000
big2 = (
    [[1, i, i + 1] for i in range(1, N_MID)]
    + [[2, i, i + 1] for i in range(1, N_MID)]
    + [[3, 1, N_MID]]
)

cases = [
    # examples
    (4, [[3, 1, 2], [3, 2, 3], [1, 1, 3], [1, 2, 4], [1, 1, 2], [2, 3, 4]], 2),
    (4, [[3, 1, 2], [3, 2, 3], [1, 1, 4], [2, 1, 4]], 0),
    (4, [[3, 2, 3], [1, 1, 2], [2, 3, 4]], -1),
    # single type 3 edge
    (2, [[3, 1, 2]], 0),
    # type 3 makes type 1 and 2 edges redundant
    (2, [[1, 1, 2], [2, 1, 2], [3, 1, 2]], 2),
    # separate edges both needed
    (2, [[1, 1, 2], [2, 1, 2]], 0),
    # Bob cannot traverse
    (3, [[1, 1, 2], [1, 2, 3]], -1),
    # redundant type 3 edge
    (3, [[3, 1, 2], [3, 2, 3], [3, 1, 3]], 1),
    # type 3 chain with many redundant type 1/2 edges
    (4, [[3, 1, 2], [3, 2, 3], [3, 3, 4], [1, 1, 3], [1, 2, 4], [1, 1, 4], [2, 1, 3]], 4),
    # mixed types, nothing removable
    (3, [[3, 1, 2], [1, 2, 3], [2, 1, 3]], 0),
    # large: type 3 chain plus one extra
    (N_BIG, big1, 1),
    # large: type 1 and type 2 chains plus one type 3 closing edge
    (N_MID, big2, 2),
]

passed = 0
total = len(cases)
for idx, (n, edges, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.maxNumEdgesToRemove(n, [list(e) for e in edges])
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            shown = edges if len(edges) <= 10 else f"<{len(edges)} edges>"
            print(f"FAIL case {idx}: input=(n={n}, edges={shown}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input=(n={n}, edges=<{len(edges)} edges>), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)