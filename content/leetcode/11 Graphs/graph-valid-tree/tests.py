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
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
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


def load_attempt():
    ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List,
          "Optional": Optional, "Dict": Dict}
    lines = open("attempt.py").read().split("\n")
    # If the file has a syntax error (e.g. a malformed trailing alternative
    # class), drop everything from the nearest class/def before the error.
    for _ in range(10):
        try:
            code = compile("\n".join(lines), "attempt.py", "exec")
            break
        except SyntaxError as e:
            lineno = e.lineno or len(lines)
            cut = None
            for i in range(min(lineno - 2, len(lines) - 1), -1, -1):
                if lines[i].lstrip().startswith(("class ", "def ")):
                    cut = i
                    break
            if cut is None or cut == 0:
                raise
            lines = lines[:cut]
    else:
        raise RuntimeError("could not load attempt.py")
    exec(code, ns)
    return ns


ns = load_attempt()
sol = ns["Solution"]()
fn = getattr(sol, "validTree", None) or getattr(sol, "valid_tree")


def random_tree_edges(n):
    # deterministic pseudo-random tree
    edges = []
    x = 12345
    for i in range(1, n):
        x = (x * 1103515245 + 12345) % (2 ** 31)
        p = x % i
        edges.append([p, i] if x % 2 else [i, p])
    return edges


path2000 = [[i, i + 1] for i in range(1999)]
cycle2000 = [[i, (i + 1) % 2000] for i in range(2000)]
star2000 = [[0, i] for i in range(1, 2000)]
path_plus_chord = path2000[:-1] + [[0, 1999 - 1], [1998, 1999]]
big_cycle_isolated = [[i, (i + 1) % 1999] for i in range(1999)]  # 1999 edges, node 1999 isolated

cases = [
    (5, [[0, 1], [0, 2], [0, 3], [1, 4]], True),
    (5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]], False),
    (4, [[0, 1], [2, 3]], False),
    (1, [], True),
    (2, [], False),
    (2, [[1, 0]], True),
    (3, [[0, 1], [1, 2], [2, 0]], False),
    (4, [[0, 1], [1, 2], [2, 0]], False),  # cycle + isolated node, n-1 edges
    (4, [[3, 2], [2, 1], [1, 0]], True),  # reversed path
    (2000, path2000, True),
    (2000, cycle2000, False),
    (2000, star2000, True),
    (2000, random_tree_edges(2000), True),
    (2000, big_cycle_isolated, False),
]

passed = 0
total = len(cases)
for idx, (n, edges, expected) in enumerate(cases, 1):
    label = f"n={n}, edges={edges if len(edges) < 20 else f'<{len(edges)} edges>'}"
    try:
        got = fn(n, [list(e) for e in edges])
        if bool(got) == expected and isinstance(got, bool):
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={label}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={label}, expected={expected}, got={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)