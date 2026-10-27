import sys
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
    q = collections.deque([root])
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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict,
      "collections": collections}
exec(open("attempt.py").read(), ns)


def run(root):
    return ns["Solution"]().rightSideView(root)


def chain(n, direction):
    """Build a degenerate chain of n nodes; values cycle within [-100, 100]."""
    root = TreeNode(0)
    cur = root
    for i in range(1, n):
        node = TreeNode((i % 201) - 100)
        if direction == "left":
            cur.left = node
        else:
            cur.right = node
        cur = node
    return root


def chain_values(n):
    return [0] + [(i % 201) - 100 for i in range(1, n)]


cases = [
    # examples
    ([1, 2, 3, None, 5, None, 4], [1, 3, 4]),
    ([1, 2, 3, 4, None, None, None, 5], [1, 3, 4, 5]),
    ([1, None, 3], [1, 3]),
    # edge cases
    ([], []),
    ([7], [7]),
    ([1, 2], [1, 2]),
    ([1, 2, 3], [1, 3]),
    ([-100, -50, 100, -100, None, None, -1], [-100, 100, -1]),
    ([5, 5, 5, 5, 5, 5, 5], [5, 5, 5]),
    ([1, 2, 3, 4, 5, 6, 7], [1, 3, 7]),
    ([1, 2, 3, None, 4, None, None, None, None], [1, 3, 4]),
]

tests = [(build_tree(v), exp, v) for v, exp in cases]

# large inputs: left-leaning chain of 100 nodes, right-leaning chain of 100 nodes
tests.append((chain(100, "left"), chain_values(100), "left chain of 100 nodes"))
tests.append((chain(100, "right"), chain_values(100), "right chain of 100 nodes"))

passed = 0
total = len(tests)
for idx, (root, expected, desc) in enumerate(tests, 1):
    try:
        got = run(root)
        if list(got) == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={desc}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={desc}, expected={expected}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
