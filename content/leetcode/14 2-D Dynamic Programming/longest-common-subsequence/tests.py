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


def reference(a, b):
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if ch == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


def pseudo_random_string(n, seed, alphabet="abc"):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % (2 ** 31)
        out.append(alphabet[(x >> 8) % len(alphabet)])
    return "".join(out)


rand_a = pseudo_random_string(1000, 1)
rand_b = pseudo_random_string(1000, 2)

cases = [
    ("abcde", "ace", 3),
    ("abc", "abc", 3),
    ("abc", "def", 0),
    ("a", "a", 1),
    ("a", "b", 0),
    ("abcdef", "xyzabcdefxyz", 6),
    ("aaaa", "aa", 2),
    ("abcbdab", "bdcaba", 4),
    ("aggtab", "gxtxayb", 4),
    ("oxcpqrsvwf", "shmtulqrypy", 2),
    ("abc", "cba", 1),
    ("a" * 1000, "a" * 1000, 1000),
    ("a" * 1000, "b" * 1000, 0),
    (rand_a, rand_b, reference(rand_a, rand_b)),
]


def run():
    solution = ns["Solution"]()
    passed = 0
    for n, (t1, t2, expected) in enumerate(cases, 1):
        shown = f"text1={t1!r}, text2={t2!r}" if len(t1) + len(t2) <= 60 else f"text1=<len {len(t1)}>, text2=<len {len(t2)}>"
        try:
            got = solution.longestCommonSubsequence(t1, t2)
        except Exception as e:
            print(f"FAIL case {n}: input={shown}, error={type(e).__name__}: {e}")
            continue
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            print(f"FAIL case {n}: input={shown}, expected={expected}, got={got}")
    print(f"{passed}/{len(cases)} passed")
    if passed != len(cases):
        sys.exit(1)


run()