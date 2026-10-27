import sys
import random
from collections import OrderedDict
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
LRUCache = ns["LRUCache"]


def reference(ops, args):
    """Expected outputs computed with OrderedDict (used for large cases)."""
    out = []
    cache = OrderedDict()
    cap = 0
    for op, a in zip(ops, args):
        if op == "LRUCache":
            cap = a[0]
            out.append(None)
        elif op == "get":
            if a[0] in cache:
                cache.move_to_end(a[0])
                out.append(cache[a[0]])
            else:
                out.append(-1)
        else:
            cache[a[0]] = a[1]
            cache.move_to_end(a[0])
            if len(cache) > cap:
                cache.popitem(last=False)
            out.append(None)
    return out


N = None
cases = []


def add(ops, args, expected):
    cases.append((ops, args, expected))


# 1: example 1
add(["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"],
    [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]],
    [N, N, N, 1, N, -1, N, -1, 3, 4])

# 2: example 2
add(["LRUCache", "put", "put", "put", "get", "get"],
    [[1], [1, 10], [1, 20], [2, 5], [1], [2]],
    [N, N, N, N, -1, 5])

# 3: capacity 1
add(["LRUCache", "put", "put", "get", "get", "put", "get", "get"],
    [[1], [1, 1], [2, 2], [1], [2], [3, 3], [2], [3]],
    [N, N, N, -1, 2, N, -1, 3])

# 4: get refreshes recency
add(["LRUCache", "put", "put", "get", "put", "get", "get", "get"],
    [[2], [1, 1], [2, 2], [1], [3, 3], [2], [1], [3]],
    [N, N, N, 1, N, -1, 1, 3])

# 5: put on existing key refreshes recency
add(["LRUCache", "put", "put", "put", "put", "get", "get", "get"],
    [[2], [1, 1], [2, 2], [1, 10], [3, 3], [2], [1], [3]],
    [N, N, N, N, N, -1, 10, 3])

# 6: updating existing key at full capacity does not evict
add(["LRUCache", "put", "put", "put", "put", "get", "get"],
    [[2], [1, 1], [2, 2], [2, 3], [1, 4], [1], [2]],
    [N, N, N, N, N, 4, 3])

# 7: get on empty cache
add(["LRUCache", "get", "get"],
    [[3], [5], [0]],
    [N, -1, -1])

# 8: key 0 / value 0 / boundary values
add(["LRUCache", "put", "get", "put", "get", "put", "get", "get", "get"],
    [[2], [0, 0], [0], [10000, 100000], [10000], [5, 5], [0], [10000], [5]],
    [N, N, 0, N, 100000, N, -1, 100000, 5])

# 9: capacity larger than number of inserts
add(["LRUCache", "put", "put", "put", "get", "get", "get", "get"],
    [[5], [1, 10], [2, 20], [3, 30], [1], [2], [3], [4]],
    [N, N, N, N, 10, 20, 30, -1])

# 10: repeatedly used key survives
add(["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get", "get"],
    [[2], [1, 1], [2, 2], [1], [3, 3], [1], [4, 4], [1], [3], [4], [2]],
    [N, N, N, 1, N, 1, N, 1, -1, 4, -1])

# 11: large random workload (performance + correctness)
rng = random.Random(12345)
ops, args = ["LRUCache"], [[3000]]
for _ in range(200000 - 1):
    if rng.random() < 0.5:
        ops.append("put")
        args.append([rng.randint(0, 5000), rng.randint(0, 100000)])
    else:
        ops.append("get")
        args.append([rng.randint(0, 5000)])
add(ops, args, reference(ops, args))

# 12: large sequential scan that thrashes the cache
ops, args = ["LRUCache"], [[3000]]
for k in range(10000):
    ops.append("put")
    args.append([k, k * 3 % 100001])
for k in range(10000):
    ops.append("get")
    args.append([k])
add(ops, args, reference(ops, args))


def short(x, limit=300):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "...(%d chars)" % len(s)


passed = 0
for i, (ops, args, expected) in enumerate(cases, 1):
    try:
        obj = None
        got = []
        for op, a in zip(ops, args):
            if op == "LRUCache":
                obj = LRUCache(*a)
                got.append(None)
            else:
                got.append(getattr(obj, op)(*a))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            bad = next(j for j in range(len(expected)) if got[j] != expected[j])
            print(f"FAIL case {i}: input={short((ops, args))}, expected={short(expected)}, "
                  f"got={short(got)} (first mismatch at op {bad}: {ops[bad]}{args[bad]})")
    except Exception as e:
        print(f"FAIL case {i}: input={short((ops, args))}, error={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)