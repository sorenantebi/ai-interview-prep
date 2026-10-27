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

# (s1, s2, expected)
cases = [
    ("ab", "eidbaooo", True),
    ("ab", "eidboaoo", False),
    ("a", "a", True),
    ("a", "b", False),
    ("abc", "ab", False),
    ("abc", "abc", True),
    ("abc", "cba", True),
    ("adc", "dcda", True),
    ("aab", "abab", True),  # window "aba" is a permutation of "aab"
    ("hello", "ooolleoooleh", False),
    ("abcd", "xxxxdcbaxx", True),
    ("aa", "ab", False),
    ("aa", "baab", True),
    ("ab" * 2500, "z" * 5000 + "ba" * 2500, True),
    ("a" * 5000, ("a" * 4999 + "b") * 2, False),  # every window of length 5000 contains a 'b'
    ("a" * 5000, "a" * 10000, True),
]


def show(s):
    return repr(s) if len(s) <= 30 else f"(len={len(s)})"


passed = 0
for n, (s1, s2, expected) in enumerate(cases, 1):
    desc = f"s1={show(s1)}, s2={show(s2)}"
    try:
        got = ns["Solution"]().checkInclusion(s1, s2)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={desc}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={desc}, error={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)