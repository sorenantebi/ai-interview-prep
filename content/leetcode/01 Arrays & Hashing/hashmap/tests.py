import sys
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


def model_expected(ops, args):
    """Ground-truth expected outputs using a plain dict model."""
    m = {}
    res = [None]
    for op, a in zip(ops[1:], args[1:]):
        if op == "put":
            m[a[0]] = a[1]
            res.append(None)
        elif op == "get":
            res.append(m.get(a[0], -1))
        else:
            m.pop(a[0], None)
            res.append(None)
    return res


cases = []

# 1: example from the problem
cases.append((
    ["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"],
    [[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]],
    [None, None, None, 1, -1, None, 1, None, -1],
))

# 2: get on empty map
cases.append((
    ["MyHashMap", "get", "get"],
    [[], [0], [1000000]],
    [None, -1, -1],
))

# 3: key 0 and value 0
cases.append((
    ["MyHashMap", "put", "get", "remove", "get"],
    [[], [0, 0], [0], [0], [0]],
    [None, None, 0, None, -1],
))

# 4: colliding keys (same bucket for common bucket counts)
cases.append((
    ["MyHashMap", "put", "put", "put", "put", "get", "get", "get", "get", "remove", "get", "get", "get"],
    [[], [1, 10], [1001, 20], [2001, 30], [1009, 40], [1], [1001], [2001], [1009], [1001], [1001], [1], [2001]],
    [None, None, None, None, None, 10, 20, 30, 40, None, -1, 10, 30],
))

# 5: repeated overwrite
cases.append((
    ["MyHashMap", "put", "put", "put", "get", "remove", "get"],
    [[], [5, 1], [5, 2], [5, 3], [5], [5], [5]],
    [None, None, None, None, 3, None, -1],
))

# 6: remove of a missing key
cases.append((
    ["MyHashMap", "remove", "put", "remove", "get"],
    [[], [7], [7, 7], [8], [7]],
    [None, None, None, None, 7],
))

# 7: maximum key and value
cases.append((
    ["MyHashMap", "put", "get", "get", "remove", "get"],
    [[], [1000000, 1000000], [1000000], [999999], [1000000], [1000000]],
    [None, None, 1000000, -1, None, -1],
))

# 8: re-put after remove
cases.append((
    ["MyHashMap", "put", "remove", "get", "put", "get"],
    [[], [3, 3], [3], [3], [3, 4], [3]],
    [None, None, None, -1, None, 4],
))

# 9: double remove
cases.append((
    ["MyHashMap", "put", "remove", "remove", "get"],
    [[], [2, 2], [2], [2], [2]],
    [None, None, None, None, -1],
))

# 10: remove middle of a chain, neighbours stay intact
cases.append((
    ["MyHashMap", "put", "put", "put", "remove", "get", "get", "get", "remove", "get", "get"],
    [[], [10, 1], [1010, 2], [2010, 3], [1010], [10], [1010], [2010], [10], [10], [2010]],
    [None, None, None, None, None, 1, -1, 3, None, -1, 3],
))

# 11: long single-bucket chain (all keys multiples of 1000)
ops = ["MyHashMap"]
args = [[]]
for i in range(1001):
    ops.append("put")
    args.append([i * 1000, i])
for i in range(1001):
    ops.append("get")
    args.append([i * 1000])
for i in range(0, 1001, 2):
    ops.append("remove")
    args.append([i * 1000])
for i in range(1001):
    ops.append("get")
    args.append([i * 1000])
exp = [None] + [None] * 1001 + list(range(1001)) + [None] * 501 + [-1 if i % 2 == 0 else i for i in range(1001)]
cases.append((ops, args, exp))

# 12: seeded random mixed operations (10^4 calls), checked against a dict model
rnd = random.Random(12345)
ops = ["MyHashMap"]
args = [[]]
for _ in range(9999):
    r = rnd.random()
    k = rnd.randint(0, 1500)
    if r < 0.4:
        ops.append("put")
        args.append([k, rnd.randint(0, 1000000)])
    elif r < 0.75:
        ops.append("get")
        args.append([k])
    else:
        ops.append("remove")
        args.append([k])
cases.append((ops, args, model_expected(ops, args)))


def run_case(ops, args):
    obj = ns[ops[0]](*args[0])
    out = [None]
    for op, a in zip(ops[1:], args[1:]):
        out.append(getattr(obj, op)(*a))
    return out


def short(x, n=300):
    s = repr(x)
    return s if len(s) <= n else s[:n] + "...(truncated)"


passed = 0
total = len(cases)
for idx, (ops, args, expected) in enumerate(cases, 1):
    try:
        got = run_case(ops, args)
        if got == expected:
            passed += 1
            print(f"PASS case {idx}")
        else:
            bad = next((i for i, (g, e) in enumerate(zip(got, expected)) if g != e), None)
            print(f"FAIL case {idx}: input={short((ops, args))}, expected={short(expected)}, got={short(got)}"
                  + (f" (first mismatch at call {bad})" if bad is not None else ""))
    except Exception as e:
        print(f"FAIL case {idx}: input={short((ops, args))}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)