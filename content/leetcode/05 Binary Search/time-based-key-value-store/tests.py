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
    out, queue = [], [root]
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


def brute_expected(ops, args):
    """Straightforward model used to derive expected outputs."""
    store = {}
    out = []
    for op, a in zip(ops, args):
        if op == "TimeMap":
            out.append(None)
        elif op == "set":
            key, value, ts = a
            store.setdefault(key, []).append((ts, value))
            out.append(None)
        else:
            key, ts = a
            res = ""
            for t, v in store.get(key, []):
                if t <= ts:
                    res = v
            out.append(res)
    return out


def replay(ops, args):
    obj = None
    out = []
    for op, a in zip(ops, args):
        if op == "TimeMap":
            obj = ns["TimeMap"](*a)
            out.append(None)
        elif op == "set":
            obj.set(*a)
            out.append(None)
        elif op == "get":
            out.append(obj.get(*a))
        else:
            raise ValueError("unknown op " + op)
    return out


def make_cases():
    cases = []

    # 1: example 1
    cases.append((
        ["TimeMap", "set", "get", "get", "set", "get", "get"],
        [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]],
        [None, None, "bar", "bar", None, "bar2", "bar2"],
    ))
    # 2: example 2
    cases.append((
        ["TimeMap", "set", "get"],
        [[], ["k", "v", 10], ["k", 5]],
        [None, None, ""],
    ))
    # 3: unknown key
    cases.append((
        ["TimeMap", "get", "set", "get"],
        [[], ["nokey", 1], ["a", "x", 1], ["b", 100]],
        [None, "", None, ""],
    ))
    # 4: single element, exact timestamp
    cases.append((
        ["TimeMap", "set", "get"],
        [[], ["a", "b", 1], ["a", 1]],
        [None, None, "b"],
    ))
    # 5: duplicate values across timestamps
    ops = ["TimeMap", "set", "set", "set", "get", "get", "get", "get"]
    args = [[], ["k", "same", 1], ["k", "same", 2], ["k", "diff", 3],
            ["k", 1], ["k", 2], ["k", 3], ["k", 4]]
    cases.append((ops, args, [None, None, None, None, "same", "same", "diff", "diff"]))
    # 6: multiple keys interleaved
    ops = ["TimeMap", "set", "set", "set", "set", "get", "get", "get", "get", "get"]
    args = [[], ["a", "a1", 1], ["b", "b1", 2], ["a", "a2", 3], ["b", "b2", 4],
            ["a", 2], ["b", 3], ["a", 10], ["b", 10], ["c", 10]]
    cases.append((ops, args, brute_expected(ops, args)))
    # 7: get before earliest timestamp
    ops = ["TimeMap", "set", "set", "get", "get"]
    args = [[], ["k", "v1", 5], ["k", "v2", 8], ["k", 4], ["k", 1]]
    cases.append((ops, args, [None, None, None, "", ""]))
    # 8: get between and after entries
    ops = ["TimeMap", "set", "set", "set", "get", "get", "get", "get", "get"]
    args = [[], ["k", "x", 10], ["k", "y", 20], ["k", "z", 30],
            ["k", 9], ["k", 15], ["k", 25], ["k", 30], ["k", 1000]]
    cases.append((ops, args, [None, None, None, None, "", "x", "y", "z", "z"]))
    # 9: interleaved set/get on same key (later sets do not affect earlier gets)
    ops = ["TimeMap", "set", "get", "set", "get", "get", "set", "get", "get"]
    args = [[], ["k", "a", 1], ["k", 5], ["k", "b", 6], ["k", 5], ["k", 6],
            ["k", "c", 7], ["k", 6], ["k", 7]]
    cases.append((ops, args, [None, None, "a", None, "a", "b", None, "b", "c"]))
    # 10: timestamp upper bound
    ops = ["TimeMap", "set", "set", "get", "get", "get"]
    args = [[], ["k", "lo", 1], ["k", "hi", 10 ** 7], ["k", 10 ** 7 - 1], ["k", 10 ** 7], ["k", 1]]
    cases.append((ops, args, [None, None, None, "lo", "hi", "lo"]))
    # 11: alphanumeric / long key and value
    long_key = "k" * 100
    long_val = "v1" * 50
    ops = ["TimeMap", "set", "get", "get"]
    args = [[], [long_key, long_val, 3], [long_key, 3], [long_key[:-1], 3]]
    cases.append((ops, args, [None, None, long_val, ""]))
    # 12: many entries for one key, random gets
    rnd = random.Random(1)
    ops = ["TimeMap"]
    args = [[]]
    ts = 0
    for i in range(200):
        ts += rnd.randint(1, 5)
        ops.append("set")
        args.append(["key", "v%d" % i, ts])
    for _ in range(300):
        ops.append("get")
        args.append(["key", rnd.randint(0, ts + 5)])
    cases.append((ops, args, brute_expected(ops, args)))
    # 13: large input for performance
    rnd = random.Random(2)
    ops = ["TimeMap"]
    args = [[]]
    ts = 0
    n_set = 100000
    for i in range(n_set):
        ts += rnd.randint(1, 50)
        ops.append("set")
        args.append(["big" if i % 10 else "other", "v%d" % i, ts])
    queries = [rnd.randint(0, ts + 10) for _ in range(100000)]
    for q in queries:
        ops.append("get")
        args.append(["big", q])
    cases.append((ops, args, None))  # expected computed with bisect below
    return cases


def fast_expected(ops, args):
    import bisect
    times, vals = {}, {}
    out = []
    for op, a in zip(ops, args):
        if op == "set":
            times.setdefault(a[0], []).append(a[2])
            vals.setdefault(a[0], []).append(a[1])
            out.append(None)
        elif op == "get":
            t = times.get(a[0], [])
            i = bisect.bisect_right(t, a[1]) - 1
            out.append(vals[a[0]][i] if i >= 0 else "")
        else:
            out.append(None)
    return out


def short(x, limit=200):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "..."


def main():
    cases = make_cases()
    passed = 0
    for n, (ops, args, expected) in enumerate(cases, 1):
        if expected is None:
            expected = fast_expected(ops, args)
        try:
            got = replay(ops, args)
        except Exception as e:
            print("FAIL case %d: input=ops=%s, args=%s, error=%s: %s"
                  % (n, short(ops), short(args), type(e).__name__, e))
            continue
        if got == expected:
            passed += 1
            print("PASS case %d" % n)
        else:
            diffs = [(i, e, g) for i, (e, g) in enumerate(zip(expected, got)) if e != g][:3]
            print("FAIL case %d: input=ops=%s, args=%s, expected=%s, got=%s, first diffs (idx, exp, got)=%s"
                  % (n, short(ops), short(args), short(expected), short(got), diffs))
    print("%d/%d passed" % (passed, len(cases)))
    if passed != len(cases):
        sys.exit(1)


main()