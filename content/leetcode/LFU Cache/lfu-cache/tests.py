import sys
import random
from typing import List, Optional, Dict
from collections import OrderedDict, defaultdict


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


# ---- reference models used to generate expected output for generated cases ----

class BruteLFU:
    def __init__(self, capacity):
        self.cap = capacity
        self.d = {}  # key -> [value, freq, tick]
        self.tick = 0

    def get(self, key):
        self.tick += 1
        if key not in self.d:
            return -1
        e = self.d[key]
        e[1] += 1
        e[2] = self.tick
        return e[0]

    def put(self, key, value):
        self.tick += 1
        if key in self.d:
            e = self.d[key]
            e[0] = value
            e[1] += 1
            e[2] = self.tick
            return
        if len(self.d) == self.cap:
            victim = min(self.d, key=lambda k: (self.d[k][1], self.d[k][2]))
            del self.d[victim]
        self.d[key] = [value, 1, self.tick]


class RefLFU:
    def __init__(self, capacity):
        self.cap = capacity
        self.vals = {}
        self.freq = {}
        self.buckets = defaultdict(OrderedDict)
        self.min_freq = 0

    def _touch(self, key):
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq += 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key):
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key, value):
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) == self.cap:
            evict, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[evict]
            del self.freq[evict]
        self.vals[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1


def make_case(cap, calls, model):
    """calls: list of ('put', k, v) or ('get', k). Returns (ops, args, expected)."""
    m = model(cap)
    ops, args, exp = ["LFUCache"], [[cap]], [None]
    for c in calls:
        if c[0] == "put":
            m.put(c[1], c[2])
            ops.append("put")
            args.append([c[1], c[2]])
            exp.append(None)
        else:
            ops.append("get")
            args.append([c[1]])
            exp.append(m.get(c[1]))
    return ops, args, exp


def random_calls(seed, n, key_range, val_range=10**9):
    r = random.Random(seed)
    calls = []
    for _ in range(n):
        if r.random() < 0.5:
            calls.append(("put", r.randint(0, key_range), r.randint(0, val_range)))
        else:
            calls.append(("get", r.randint(0, key_range)))
    return calls


# ---- build cases ----

cases = []

# 1-3: examples from the problem statement
cases.append((
    ["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"],
    [[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]],
    [None, None, None, 1, None, -1, 3, None, -1, 3, 4],
))
cases.append((
    ["LFUCache", "put", "get", "put", "get", "get"],
    [[1], [1, 10], [1], [2, 20], [1], [2]],
    [None, None, 10, None, -1, 20],
))
cases.append((
    ["LFUCache", "put", "put", "put", "put", "get", "get", "get"],
    [[2], [1, 1], [2, 2], [1, 5], [3, 3], [2], [1], [3]],
    [None, None, None, None, None, -1, 5, 3],
))

# 4: get on an empty cache
cases.append((
    ["LFUCache", "get", "get"],
    [[3], [0], [100000]],
    [None, -1, -1],
))

# 5: capacity 1, repeated puts of same key then a new key
cases.append((
    ["LFUCache", "put", "put", "put", "get", "put", "get", "get"],
    [[1], [5, 1], [5, 2], [5, 3], [5], [6, 7], [5], [6]],
    [None, None, None, None, 3, None, -1, 7],
))

# 6: LRU tie-break among equal frequencies (all at freq 1)
cases.append((
    ["LFUCache", "put", "put", "put", "put", "get", "get", "get", "get"],
    [[3], [1, 1], [2, 2], [3, 3], [4, 4], [1], [2], [3], [4]],
    [None, None, None, None, None, -1, 2, 3, 4],
))

# 7: key 0 and value 0 are valid
cases.append((
    ["LFUCache", "put", "get", "put", "put", "get", "get", "get"],
    [[2], [0, 0], [0], [1, 1], [2, 2], [0], [1], [2]],
    [None, None, 0, None, None, 0, -1, 2],
))

# 8: evicted key re-inserted starts from count 1 again
cases.append((
    ["LFUCache", "put", "put", "get", "get", "put", "put", "get", "get", "get"],
    [[2], [1, 1], [2, 2], [1], [1], [3, 3], [2, 22], [3], [1], [2]],
    [None, None, None, 1, 1, None, None, -1, 1, 22],
))

# 9: put on existing key counts as a use and protects it
cases.append((
    ["LFUCache", "put", "put", "put", "put", "get", "get", "get"],
    [[2], [1, 1], [2, 2], [2, 20], [3, 3], [1], [2], [3]],
    [None, None, None, None, None, -1, 20, 3],
))

# 10: random, capacity 3, small key space (brute force model)
cases.append(make_case(3, random_calls(1, 2000, 8), BruteLFU))

# 11: random, capacity 1
cases.append(make_case(1, random_calls(2, 1000, 4), BruteLFU))

# 12: random, capacity 10, wider key space
cases.append(make_case(10, random_calls(3, 3000, 30), BruteLFU))

# 13: performance, capacity 10^4, 2*10^5 calls, keys up to 10^5
cases.append(make_case(10**4, random_calls(4, 2 * 10**5 - 1, 20000), RefLFU))

# ---- load solution ----

ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def short(x, limit=300):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "...(%d chars)" % len(s)


def run_case(ops, args):
    cls = ns["LFUCache"]
    obj = None
    out = []
    for op, a in zip(ops, args):
        if op == "LFUCache":
            obj = cls(*a)
            out.append(None)
        else:
            out.append(getattr(obj, op)(*a))
    return out


passed = 0
total = len(cases)
for i, (ops, args, expected) in enumerate(cases, 1):
    try:
        got = run_case(ops, args)
    except Exception as e:
        print("FAIL case %d: input=%s, error=%s: %s" % (i, short(list(zip(ops, args))), type(e).__name__, e))
        continue
    if got == expected:
        passed += 1
        print("PASS case %d" % i)
    else:
        idx = next((j for j in range(min(len(got), len(expected))) if got[j] != expected[j]), None)
        detail = "" if idx is None else " (first mismatch at op %d: %s%s)" % (idx, ops[idx], args[idx])
        print("FAIL case %d: input=%s, expected=%s, got=%s%s" % (
            i, short(list(zip(ops, args))), short(expected), short(got), detail))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)