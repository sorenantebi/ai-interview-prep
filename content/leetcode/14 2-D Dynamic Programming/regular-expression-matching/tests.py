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
Solution = ns["Solution"]


CASES = [
    # (s, p, expected)
    ("aa", "a", False),                      # example 1
    ("aa", "a*", True),                      # example 2
    ("ab", ".*", True),                      # example 3
    ("a", "a", True),                        # single char match
    ("a", "b", False),                       # single char mismatch
    ("aab", "c*a*b", True),                  # star matching zero copies
    ("mississippi", "mis*is*p*.", False),    # classic false
    ("mississippi", "mis*is*ip*.", True),    # classic true
    ("ab", ".*c", False),                    # trailing literal unmatched
    ("aaa", "a*a", True),                    # star must give back a char
    ("aaa", "ab*a*c*a", True),               # multiple stars, zero copies
    ("a", "ab*", True),                      # star at end matches zero
    ("abc", "a.c", True),                    # dot wildcard
    ("abc", "a.", False),                    # pattern too short
    ("a" * 20, "a*" * 10, True),             # stress: many stars
    ("a" * 20, "a*" * 9 + "b", False),       # stress: backtracking blow-up
    ("a" * 19 + "b", ".*" * 10, True),       # stress: many dot-stars
]


def main():
    passed = 0
    total = len(CASES)
    for idx, (s, p, expected) in enumerate(CASES, 1):
        try:
            got = Solution().isMatch(s, p)
            if got is expected or (isinstance(got, bool) and got == expected):
                print(f"PASS case {idx}")
                passed += 1
            else:
                print(f"FAIL case {idx}: input=(s={s!r}, p={p!r}), expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {idx}: input=(s={s!r}, p={p!r}), expected={expected}, got=exception: {type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()