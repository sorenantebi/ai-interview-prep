import sys
from itertools import permutations
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


def canon(perms):
    return sorted(tuple(p) for p in perms)


def expected_for(nums):
    return sorted(permutations(nums))


CASES = [
    [1, 2, 3],                  # example 1
    [0, 1],                     # example 2
    [1],                        # example 3 / single element
    [-1, 0, 1],                 # negatives
    [-10, 10],                  # bounds
    [5, -5],                    # two negatives/positives
    [3, 2, 1],                  # descending input
    [0],                        # single zero
    [-3, -2, -1, 0],            # all non-positive
    [1, 2, 3, 4],               # n=4
    [10, -10, 0, 5, -5],        # n=5 mixed
    [1, 2, 3, 4, 5, 6],         # max size
    [-10, 10, 0, 7, -7, 3],     # max size mixed
]


def run():
    passed = 0
    total = len(CASES)
    for idx, nums in enumerate(CASES, 1):
        exp = expected_for(nums)
        try:
            sol = ns["Solution"]()
            got = sol.permute(list(nums))
            got_c = canon(got)
            if got_c == [tuple(e) for e in exp]:
                print(f"PASS case {idx}")
                passed += 1
            else:
                print(f"FAIL case {idx}: input={nums}, expected={[list(e) for e in exp]}, got={got}")
        except Exception as e:
            print(f"FAIL case {idx}: input={nums}, error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()