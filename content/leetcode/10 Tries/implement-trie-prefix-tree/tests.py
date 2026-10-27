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


def build_list(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    qi = 0
    while qi < len(queue) and i < len(arr):
        node = queue[qi]
        qi += 1
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if root is None:
        return []
    out = []
    queue = [root]
    qi = 0
    while qi < len(queue):
        node = queue[qi]
        qi += 1
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


def run_ops(ops, args):
    trie = None
    res = []
    for op, a in zip(ops, args):
        if op == "Trie":
            trie = ns["Trie"](*a)
            res.append(None)
        else:
            res.append(getattr(trie, op)(*a))
    return res


def make_ops(seq):
    """seq: list of (op, arg-or-None, expected). Returns ops, args, expected."""
    ops = ["Trie"]
    args = [[]]
    exp = [None]
    for op, arg, e in seq:
        ops.append(op)
        args.append([arg])
        exp.append(e)
    return ops, args, exp


cases = []

# 1: Example 1
cases.append(make_ops([
    ("insert", "apple", None),
    ("search", "apple", True),
    ("search", "app", False),
    ("startsWith", "app", True),
    ("insert", "app", None),
    ("search", "app", True),
]))

# 2: Example 2
cases.append(make_ops([
    ("insert", "a", None),
    ("startsWith", "b", False),
    ("search", "a", True),
]))

# 3: empty trie
cases.append(make_ops([
    ("search", "a", False),
    ("startsWith", "a", False),
    ("search", "hello", False),
]))

# 4: duplicate inserts
cases.append(make_ops([
    ("insert", "dup", None),
    ("insert", "dup", None),
    ("search", "dup", True),
    ("search", "du", False),
    ("startsWith", "dup", True),
]))

# 5: word longer than inserted
cases.append(make_ops([
    ("insert", "app", None),
    ("search", "apple", False),
    ("startsWith", "apple", False),
    ("startsWith", "app", True),
]))

# 6: shared prefixes, multiple words
cases.append(make_ops([
    ("insert", "car", None),
    ("insert", "card", None),
    ("insert", "care", None),
    ("insert", "cat", None),
    ("search", "car", True),
    ("search", "ca", False),
    ("search", "card", True),
    ("search", "cards", False),
    ("startsWith", "ca", True),
    ("startsWith", "cat", True),
    ("startsWith", "cab", False),
    ("startsWith", "d", False),
]))

# 7: single characters
cases.append(make_ops([
    ("insert", "a", None),
    ("insert", "z", None),
    ("search", "a", True),
    ("search", "z", True),
    ("search", "m", False),
    ("startsWith", "z", True),
    ("startsWith", "zz", False),
]))

# 8: prefix inserted before the longer word
cases.append(make_ops([
    ("insert", "a", None),
    ("insert", "ab", None),
    ("insert", "abc", None),
    ("search", "a", True),
    ("search", "ab", True),
    ("search", "abc", True),
    ("search", "abcd", False),
    ("startsWith", "abc", True),
]))

# 9: diverging branches
cases.append(make_ops([
    ("insert", "abc", None),
    ("insert", "abd", None),
    ("search", "ab", False),
    ("search", "abe", False),
    ("startsWith", "ab", True),
    ("startsWith", "abe", False),
    ("startsWith", "b", False),
]))

# 10: max length word
long_word = "a" * 1999 + "b"
cases.append(make_ops([
    ("insert", long_word, None),
    ("search", long_word, True),
    ("search", "a" * 2000, False),
    ("search", "a" * 1999, False),
    ("startsWith", "a" * 1999, True),
    ("startsWith", "a" * 2000, False),
    ("startsWith", long_word, True),
]))


# 11: many operations (performance)
def perf_case():
    seq = []
    words = []
    for i in range(5000):
        w = ""
        n = i
        for _ in range(6):
            w += chr(ord("a") + n % 26)
            n //= 26
        words.append(w)
    for w in words:
        seq.append(("insert", w, None))
    for w in words[:5000]:
        seq.append(("search", w, True))
    for w in words[:5000]:
        seq.append(("startsWith", w[:3], True))
    for w in words[:5000]:
        seq.append(("search", w[:5], False))
    return make_ops(seq)


cases.append(perf_case())

# 12: several long words sharing a long prefix
base = "x" * 1000
cases.append(make_ops([
    ("insert", base + "a", None),
    ("insert", base + "b", None),
    ("search", base, False),
    ("search", base + "a", True),
    ("search", base + "b", True),
    ("search", base + "c", False),
    ("startsWith", base, True),
    ("startsWith", base + "c", False),
]))

passed = 0
total = len(cases)
for n, (ops, args, exp) in enumerate(cases, 1):
    try:
        got = run_ops(ops, args)
        if got == exp:
            passed += 1
            print(f"PASS case {n}")
        else:
            if len(ops) > 20:
                idx = next(i for i, (g, e) in enumerate(zip(got, exp)) if g != e)
                print(f"FAIL case {n}: input=({len(ops)} ops), first mismatch at op #{idx} "
                      f"{ops[idx]}({args[idx][0][:30] if args[idx] else ''}), expected={exp[idx]}, got={got[idx]}")
            else:
                short_args = [[(a[:30] + "...") if isinstance(a, str) and len(a) > 30 else a for a in aa] for aa in args]
                short_exp = exp
                print(f"FAIL case {n}: input={ops} {short_args}, expected={short_exp}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input=({len(ops)} ops), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)