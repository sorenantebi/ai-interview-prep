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


def list_to_py(head):
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


def tree_to_list(root):
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


def ref(n):
    return int(format(n, "032b")[::-1], 2)


# (input n, expected)
CASES = [
    (43261596, 964176192),            # example 1
    (2147483644, 1073741822),         # example 2
    (0, 0),                           # all zeros
    (1, 2147483648),                  # lowest bit -> highest bit
    (2147483648, 1),                  # highest bit -> lowest bit
    (4294967295, 4294967295),         # all ones
    (2, 1073741824),                  # even, single bit
    (4, 536870912),
    (2863311530, 1431655765),         # 0xAAAAAAAA -> 0x55555555
    (4042322160, 252645135),          # 0xF0F0F0F0 -> 0x0F0F0F0F
    (4294901760, 65535),              # 0xFFFF0000 -> 0x0000FFFF
    (2147483649, 2147483649),         # palindromic bit pattern
]


def run():
    passed = 0
    total = 0
    for n, expected in CASES:
        total += 1
        try:
            got = ns["Solution"]().reverseBits(n)
            if got == expected:
                print(f"PASS case {total}")
                passed += 1
            else:
                print(f"FAIL case {total}: input={n}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {total}: input={n}, expected={expected}, got=Exception: {e}")

    # Many calls (performance / follow-up) compared against an independent reference
    total += 1
    import random
    rng = random.Random(12345)
    inputs = [rng.randrange(0, 2 ** 32) for _ in range(20000)]
    try:
        sol = ns["Solution"]()
        bad = None
        for n in inputs:
            got = sol.reverseBits(n)
            if got != ref(n):
                bad = (n, ref(n), got)
                break
        if bad is None:
            print(f"PASS case {total}")
            passed += 1
        else:
            print(f"FAIL case {total}: input={bad[0]}, expected={bad[1]}, got={bad[2]}")
    except Exception as e:
        print(f"FAIL case {total}: input=20000 random values, expected=reference, got=Exception: {e}")

    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()
