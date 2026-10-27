import sys
import copy
import random
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


def reference(n, flights, src, dst, k):
    inf = float("inf")
    prices = [inf] * n
    prices[src] = 0
    for _ in range(k + 1):
        tmp = prices.copy()
        for s, d, p in flights:
            if prices[s] != inf and prices[s] + p < tmp[d]:
                tmp[d] = prices[s] + p
        prices = tmp
    return -1 if prices[dst] == inf else prices[dst]


def brute(n, flights, src, dst, k):
    # independent DFS check for small graphs
    adj = {}
    for s, d, p in flights:
        adj.setdefault(s, []).append((d, p))
    best = [float("inf")]

    def dfs(u, flights_used, cost):
        if u == dst:
            best[0] = min(best[0], cost)
            return
        if flights_used == k + 1:
            return
        for v, p in adj.get(u, []):
            dfs(v, flights_used + 1, cost + p)

    dfs(src, 0, 0)
    return -1 if best[0] == float("inf") else best[0]


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = []

# Examples
cases.append((4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1, 700))
cases.append((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1, 200))
cases.append((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0, 500))

# No flights at all
cases.append((2, [], 0, 1, 0, -1))
# Direct flight only
cases.append((2, [[0, 1, 5]], 0, 1, 0, 5))
# Unreachable: wrong direction
cases.append((3, [[1, 0, 10], [2, 1, 10]], 0, 2, 2, -1))
# Route exists but needs more stops than allowed
cases.append((4, [[0, 1, 1], [1, 2, 1], [2, 3, 1]], 0, 3, 1, -1))
# Route needs exactly k stops
cases.append((4, [[0, 1, 1], [1, 2, 1], [2, 3, 1]], 0, 3, 2, 3))
# Cycle with cheaper long path blocked by k, cheap path with more stops allowed
cases.append((5, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1], [0, 4, 100]], 0, 4, 2, 100))
cases.append((5, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1], [0, 4, 100]], 0, 4, 3, 4))
# Cycles shouldn't confuse
cases.append((3, [[0, 1, 10], [1, 0, 10], [1, 2, 10]], 0, 2, 5, 20))

# Large: complete directed graph, n=100
rng = random.Random(12345)
n = 100
flights = [[i, j, rng.randint(1, 10000)] for i in range(n) for j in range(n) if i < j]
cases.append((n, flights, 0, 99, 98, reference(n, flights, 0, 99, 98)))

# Large: chain of 100 cities, performance and exact k
chain = [[i, i + 1, 10000] for i in range(99)]
cases.append((100, chain, 0, 99, 98, 99 * 10000))

# Random small graphs cross-checked with brute force
rng2 = random.Random(7)
n = 6
pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
rf = [[a, b, rng2.randint(1, 20)] for a, b in rng2.sample(pairs, 14)]
cases.append((n, rf, 0, 5, 2, brute(n, rf, 0, 5, 2)))

passed = 0
total = len(cases)
for idx, (n, flights, src, dst, k, expected) in enumerate(cases, 1):
    inp = f"n={n}, flights={flights if len(flights) <= 20 else f'<{len(flights)} flights>'}, src={src}, dst={dst}, k={k}"
    try:
        got = ns["Solution"]().findCheapestPrice(n, copy.deepcopy(flights), src, dst, k)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={inp}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={inp}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)