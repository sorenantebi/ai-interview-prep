import sys
import random
import time
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


def reference(target, position, speed):
    # exact integer arithmetic: time a = (target-pa)/sa, compare via cross-multiplication
    cars = sorted(zip(position, speed), reverse=True)
    count = 0
    last_d, last_s = None, None
    for p, s in cars:
        d = target - p
        if last_d is None or d * last_s > last_d * s:
            count += 1
            last_d, last_s = d, s
    return count


def random_case(rng, n, target, max_speed):
    position = rng.sample(range(target), n)
    speed = [rng.randint(1, max_speed) for _ in range(n)]
    return target, position, speed


rng = random.Random(12345)
big_n = 100000
rand_small = random_case(rng, 8, 50, 10)
rand_mid = random_case(rng, 1000, 10**6, 1000)
rand_big = random_case(rng, big_n, 10**6, 10**6)

T = 10**6
cases = [
    # (target, position, speed, expected)
    (12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3], 3),
    (10, [3], [3], 1),
    (100, [0, 2, 4], [4, 2, 1], 1),
    # two cars, rear is never faster -> two fleets
    (10, [0, 5], [1, 1], 2),
    # catch up exactly at destination -> same fleet
    (10, [6, 0], [2, 5], 1),
    # unsorted input
    (10, [0, 4, 2], [2, 1, 3], 1),
    # all separate fleets
    (10, [0, 1, 2, 3], [1, 2, 3, 4], 4),
    # fast rear car merges, slow middle car stays separate from front
    (20, [0, 10, 15], [10, 1, 1], 2),
    # single car at extremes
    (T, [0], [T], 1),
    # random small, exact reference
    (*rand_small, reference(*rand_small)),
    # random mid, exact reference
    (*rand_mid, reference(*rand_mid)),
    # large: every car has time 1 -> one fleet
    (T, list(range(100000)), [T - i for i in range(100000)], 1),
    # large: equal speed, distinct positions -> every car its own fleet
    (big_n, list(range(big_n)), [1] * big_n, big_n),
    # large random, exact reference
    (*rand_big, reference(*rand_big)),
]

passed = 0
total = len(cases)
for i, (target, position, speed, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.carFleet(target, list(position), list(speed))
        if got == expected:
            passed += 1
            print(f"PASS case {i}")
        else:
            inp = f"target={target}, position={position}, speed={speed}"
            if len(inp) > 200:
                inp = inp[:200] + "..."
            print(f"FAIL case {i}: input={inp}, expected={expected}, got={got}")
    except Exception as e:
        inp = f"target={target}, position={position}, speed={speed}"
        if len(inp) > 200:
            inp = inp[:200] + "..."
        print(f"FAIL case {i}: input={inp}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)