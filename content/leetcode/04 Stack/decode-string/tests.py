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

CASES = [
    ("3[a]2[bc]", "aaabcbc"),
    ("3[a2[c]]", "accaccacc"),
    ("2[abc]3[cd]ef", "abcabccdcdcdef"),
    ("abc", "abc"),
    ("1[a]", "a"),
    ("10[a]", "a" * 10),
    ("2[a2[b2[c]]]", "abccbccabccbcc"),
    ("ab2[c]de", "abccde"),
    ("300[a]", "a" * 300),
    ("2[2[2[a]]]", "a" * 8),
    ("2[a]2[b]2[c]", "aabbcc"),
    ("3[z]2[2[y]pq4[f]]", "zzzyypqffffyypqffff"),
    ("300[300[a]]", "a" * 90000),
]


def short(x):
    x = repr(x)
    return x if len(x) <= 80 else x[:77] + "..."


def main():
    passed = 0
    total = len(CASES)
    for i, (s, expected) in enumerate(CASES, 1):
        try:
            got = ns["Solution"]().decodeString(s)
            if got == expected:
                passed += 1
                print(f"PASS case {i}")
            else:
                print(f"FAIL case {i}: input={short(s)}, expected={short(expected)}, got={short(got)}")
        except Exception as e:
            print(f"FAIL case {i}: input={short(s)}, error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()