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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

N = None  # void result

# Each case is a list of (method, argument, expected_result).
cases = []

# 1. Example from the problem statement
cases.append([
    ("add", 1, N), ("add", 2, N), ("contains", 1, True), ("contains", 3, False),
    ("add", 2, N), ("contains", 2, True), ("remove", 2, N), ("contains", 2, False),
])

# 2. contains on an empty set
cases.append([("contains", 5, False), ("contains", 0, False)])

# 3. remove a key that does not exist
cases.append([
    ("remove", 7, N), ("contains", 7, False), ("add", 8, N),
    ("remove", 7, N), ("contains", 8, True),
])

# 4. key 0
cases.append([
    ("add", 0, N), ("contains", 0, True), ("contains", 1, False),
    ("remove", 0, N), ("contains", 0, False),
])

# 5. max key 10^6
cases.append([
    ("add", 1000000, N), ("contains", 1000000, True), ("contains", 999999, False),
    ("remove", 1000000, N), ("contains", 1000000, False),
])

# 6. duplicate adds, a single remove deletes the key
cases.append([
    ("add", 3, N), ("add", 3, N), ("add", 3, N), ("remove", 3, N),
    ("contains", 3, False), ("remove", 3, N), ("contains", 3, False),
])

# 7. keys that collide modulo 1009 (and other common bucket sizes)
cases.append([
    ("add", 1, N), ("add", 1010, N), ("add", 2019, N),
    ("contains", 1, True), ("contains", 1010, True), ("contains", 2019, True),
    ("remove", 1010, N), ("contains", 1010, False),
    ("contains", 1, True), ("contains", 2019, True),
])

# 8. re-add after remove
cases.append([
    ("add", 42, N), ("remove", 42, N), ("contains", 42, False),
    ("add", 42, N), ("contains", 42, True), ("remove", 42, N), ("contains", 42, False),
])

# 9. removing one key does not affect others
cases.append([
    ("add", 10, N), ("add", 20, N), ("add", 30, N), ("remove", 20, N),
    ("contains", 10, True), ("contains", 20, False), ("contains", 30, True),
    ("contains", 40, False),
])

# 10. larger workload (about 7500 operations)
big = []
for i in range(3000):
    big.append(("add", i * 7, N))
for i in range(0, 3000, 2):
    big.append(("remove", i * 7, N))
for i in range(3000):
    big.append(("contains", i * 7, i % 2 == 1))
cases.append(big)

# 11. 10^4 operations near the upper key bound
big2 = []
for i in range(2500):
    big2.append(("add", 1000000 - i, N))
for i in range(2500):
    big2.append(("contains", 1000000 - i, True))
for i in range(2500):
    big2.append(("remove", 1000000 - i, N))
for i in range(2500):
    big2.append(("contains", 1000000 - i, False))
cases.append(big2)


def short(x, limit=300):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "...(%d chars)" % len(s)


passed = 0
total = len(cases)
for idx, case in enumerate(cases, 1):
    ops = [c[0] for c in case]
    args = [c[1] for c in case]
    expected = [c[2] for c in case]
    try:
        obj = ns["MyHashSet"]()
        got = []
        for op, arg in zip(ops, args):
            res = getattr(obj, op)(arg)
            if op != "contains":
                res = None
            got.append(res)
        ok = len(got) == len(expected) and all(
            (g is e) if e is None or isinstance(e, bool) else g == e
            for g, e in zip(got, expected)
        )
        if ok:
            passed += 1
            print(f"PASS case {idx}")
        else:
            bad = next(i for i, (g, e) in enumerate(zip(got, expected))
                       if not ((g is e) if e is None or isinstance(e, bool) else g == e))
            print(f"FAIL case {idx}: input={short(list(zip(ops, args)))}, "
                  f"expected={short(expected)}, got={short(got)} (first mismatch at op {bad}: "
                  f"{ops[bad]}({args[bad]}) expected {expected[bad]}, got {got[bad]})")
    except Exception as e:
        print(f"FAIL case {idx}: input={short(list(zip(ops, args)))}, "
              f"expected={short(expected)}, got=exception {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)