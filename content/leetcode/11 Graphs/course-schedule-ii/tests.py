import sys
from typing import List, Optional, Dict

sys.setrecursionlimit(20000)


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
    out, queue = [], [root]
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


def run(n, prereqs):
    return ns["Solution"]().findOrder(n, [list(p) for p in prereqs])


def valid_order(n, prereqs, got):
    if not isinstance(got, list) or len(got) != n:
        return False
    if sorted(got) != list(range(n)):
        return False
    pos = {c: i for i, c in enumerate(got)}
    return all(pos[b] < pos[a] for a, b in prereqs)


# (n, prereqs, solvable)
cases = []
cases.append((2, [[1, 0]], True))
cases.append((4, [[1, 0], [2, 0], [3, 1], [3, 2]], True))
cases.append((1, [], True))
cases.append((2, [[1, 0], [0, 1]], False))
cases.append((3, [], True))
cases.append((4, [[1, 0], [2, 1], [1, 2]], False))
cases.append((5, [[0, 1], [1, 2], [2, 3], [3, 4]], True))
cases.append((3, [[0, 1], [1, 2], [2, 0]], False))
cases.append((6, [[1, 0], [3, 2], [5, 4]], True))
cases.append((4, [[1, 0], [2, 0], [3, 1], [3, 2], [0, 3]], False))
cases.append((2000, [[i, i - 1] for i in range(1, 2000)], True))
cases.append((200, [[j, i] for i in range(200) for j in range(i + 1, 200)], True))
cases.append((2000, [[i, i - 1] for i in range(1, 2000)] + [[0, 1999]], False))

passed = 0
total = len(cases)
for idx, (n, prereqs, solvable) in enumerate(cases, 1):
    shown = prereqs if len(prereqs) <= 20 else "<%d pairs>" % len(prereqs)
    expected = "any valid ordering" if solvable else []
    try:
        got = run(n, prereqs)
        if solvable:
            ok = valid_order(n, prereqs, got)
        else:
            ok = got == []
        if ok:
            print(f"PASS case {idx}")
            passed += 1
        else:
            shown_got = got if not isinstance(got, list) or len(got) <= 30 else f"<list of {len(got)}>"
            print(f"FAIL case {idx}: input={(n, shown)}, expected={expected}, got={shown_got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={(n, shown)}, expected={expected}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
