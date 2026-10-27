import sys
import itertools
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
    if not root:
        return []
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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

KEYPAD = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
    "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
}


def expected_for(digits):
    if not digits:
        return []
    return sorted("".join(p) for p in itertools.product(*(KEYPAD[d] for d in digits)))


CASES = [
    "23",       # example 1
    "",         # example 2
    "2",        # example 3
    "7",        # 4-letter digit
    "9",        # 4-letter digit
    "79",       # both 4-letter digits (16)
    "22",       # repeated digit
    "234",      # three digits
    "789",      # mix with 4-letter digits
    "2222",     # max length, all 3-letter
    "7777",     # max length, all 4-letter (256)
    "2579",     # mixed max length
    "9876",     # descending order
]


def main():
    passed = 0
    total = len(CASES)
    for n, digits in enumerate(CASES, 1):
        expected = expected_for(digits)
        try:
            got = ns["Solution"]().letterCombinations(digits)
            got_c = sorted(got)
            if got_c == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={digits!r}, expected={expected}, got={got_c}")
        except Exception as e:
            print(f"FAIL case {n}: input={digits!r}, error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()