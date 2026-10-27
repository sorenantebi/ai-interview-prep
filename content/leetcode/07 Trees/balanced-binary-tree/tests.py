import sys
import threading
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
    queue = [root]
    i = 1
    qi = 0
    while qi < len(queue) and i < len(vals):
        node = queue[qi]
        qi += 1
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
    qi = 0
    while qi < len(queue):
        node = queue[qi]
        qi += 1
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def skewed(n, left=True):
    root = TreeNode(0)
    cur = root
    for i in range(1, n):
        nxt = TreeNode(i)
        if left:
            cur.left = nxt
        else:
            cur.right = nxt
        cur = nxt
    return root


def perfect(depth):
    if depth == 0:
        return None
    return TreeNode(1, perfect(depth - 1), perfect(depth - 1))


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def run_case(root):
    return ns["Solution"]().isBalanced(root)


# (description, tree builder (callable returning root), expected)
CASES = [
    ("[3,9,20,null,null,15,7]", lambda: build_tree([3, 9, 20, None, None, 15, 7]), True),
    ("[1,2,2,3,3,null,null,4,4]", lambda: build_tree([1, 2, 2, 3, 3, None, None, 4, 4]), False),
    ("[]", lambda: None, True),
    ("[1]", lambda: build_tree([1]), True),
    ("[1,2]", lambda: build_tree([1, 2]), True),
    ("[1,null,2,null,3]", lambda: build_tree([1, None, 2, None, 3]), False),
    ("[1,2,null,3]", lambda: build_tree([1, 2, None, 3]), False),
    ("[1,2,2,3,null,null,3,4,null,null,4]", lambda: build_tree([1, 2, 2, 3, None, None, 3, 4, None, None, 4]), False),
    ("[1,2,3,4,5,6,7]", lambda: build_tree([1, 2, 3, 4, 5, 6, 7]), True),
    ("[1,2,3,4,null,null,5] (deep leaves, balanced at root)", lambda: build_tree([1, 2, 3, 4, None, None, 5]), True),
    ("[-1,-2,-3,-4,null,null,null,-5] (negatives, left-heavy subtree unbalanced)", lambda: build_tree([-1, -2, -3, -4, None, None, None, -5]), False),
    ("balanced at root but unbalanced deeper: [1,2,3,4,5,null,null,6,null,null,null,7]", lambda: build_tree([1, 2, 3, 4, 5, None, None, 6, None, None, None, 7]), False),
    ("perfect tree depth 12 (4095 nodes)", lambda: perfect(12), True),
    ("left-skewed chain of 5000 nodes", lambda: skewed(5000, True), False),
    ("right-skewed chain of 2 nodes", lambda: skewed(2, False), True),
]


def main():
    passed = 0
    total = len(CASES)
    for n, (desc, builder, expected) in enumerate(CASES, 1):
        try:
            got = run_case(builder())
            if got is expected or (isinstance(got, bool) and got == expected):
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={desc}, expected={expected}, got={got}")
        except BaseException as e:
            print(f"FAIL case {n}: input={desc}, expected={expected}, got=exception {type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    sys.setrecursionlimit(20000)
    threading.stack_size(256 * 1024 * 1024)
    result = {}

    def target():
        try:
            main()
            result["code"] = 0
        except SystemExit as e:
            result["code"] = e.code if isinstance(e.code, int) else 1

    t = threading.Thread(target=target)
    t.start()
    t.join()
    sys.exit(result.get("code", 1))
