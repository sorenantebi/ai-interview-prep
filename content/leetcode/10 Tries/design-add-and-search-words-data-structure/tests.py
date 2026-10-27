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


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = [root]
    i = 1
    while q and i < len(arr):
        node = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
WordDictionary = ns["WordDictionary"]


def run_ops(ops, args):
    obj = None
    out = []
    for op, a in zip(ops, args):
        if op == "WordDictionary":
            obj = WordDictionary(*a)
            out.append(None)
        elif op == "addWord":
            out.append(obj.addWord(*a))
        elif op == "search":
            out.append(obj.search(*a))
        else:
            raise ValueError("unknown op " + op)
    return out


def make_case(ops_list):
    """ops_list: list of (op, arg, expected). Constructor is added automatically."""
    ops = ["WordDictionary"]
    args = [[]]
    exp = [None]
    for op, arg, e in ops_list:
        ops.append(op)
        args.append([arg])
        exp.append(e)
    return ops, args, exp


cases = []

# 1: Example 1
cases.append(make_case([
    ("addWord", "bad", None), ("addWord", "dad", None), ("addWord", "mad", None),
    ("search", "pad", False), ("search", "bad", True),
    ("search", ".ad", True), ("search", "b..", True),
]))

# 2: Example 2
cases.append(make_case([
    ("addWord", "a", None), ("search", ".", True), ("search", "..", False),
]))

# 3: empty dictionary
cases.append(make_case([
    ("search", "a", False), ("search", ".", False), ("search", "..", False),
]))

# 4: prefix is not a word, and word is not a prefix of longer query
cases.append(make_case([
    ("addWord", "apple", None),
    ("search", "app", False), ("search", "appl.", True),
    ("search", "apple", True), ("search", "apples", False),
    ("search", "app..", True), ("search", "....", False),
]))

# 5: duplicates
cases.append(make_case([
    ("addWord", "dup", None), ("addWord", "dup", None),
    ("search", "dup", True), ("search", "d.p", True), ("search", "du", False),
]))

# 6: words that are prefixes of each other
cases.append(make_case([
    ("addWord", "a", None), ("addWord", "ab", None), ("addWord", "abc", None),
    ("search", "a", True), ("search", "ab", True), ("search", "abc", True),
    ("search", "abcd", False), ("search", ".b", True), ("search", "..c", True),
    ("search", ".bd", False),
]))

# 7: dot at start / end / both
cases.append(make_case([
    ("addWord", "hello", None), ("addWord", "world", None),
    ("search", ".ello", True), ("search", "hell.", True),
    ("search", ".orld", True), ("search", "h...o", True),
    ("search", "w...x", False), ("search", ".....", True),
    ("search", "x....", False),
]))

# 8: dot must match a letter, not nothing (length matters)
cases.append(make_case([
    ("addWord", "ab", None),
    ("search", ".", False), ("search", "..", True), ("search", "...", False),
    ("search", "a.", True), ("search", ".b", True), ("search", ".c", False),
]))

# 9: backtracking needed across branches
cases.append(make_case([
    ("addWord", "abc", None), ("addWord", "abd", None),
    ("addWord", "bbc", None), ("addWord", "cbe", None),
    ("search", ".be", True), ("search", ".bf", False),
    ("search", "a.d", True), ("search", "a.e", False),
    ("search", ".b.", True), ("search", "..e", True),
]))

# 10: max length words (25 chars)
long_word = "abcdefghijklmnopqrstuvwxy"
cases.append(make_case([
    ("addWord", long_word, None),
    ("search", long_word, True), ("search", long_word[:-1], False),
    ("search", long_word[:-1] + ".", True), ("search", "." + long_word[1:], True),
    ("search", "." + long_word[1:-1] + ".", True),
    ("search", long_word[:-1] + "z", False),
    ("search", long_word + "a", False),
]))

# 11: interleaved add and search
cases.append(make_case([
    ("search", "cat", False), ("addWord", "cat", None), ("search", "cat", True),
    ("search", "c.t", True), ("search", "c.r", False),
    ("addWord", "car", None), ("search", "c.r", True), ("search", "ca.", True),
    ("search", "..t", True),
]))

# 12: performance, many words and many queries
perf_ops = []
words = []
for i in range(5000):
    w = ""
    x = i
    for _ in range(6):
        w += chr(ord("a") + x % 26)
        x //= 26
    words.append(w)
    perf_ops.append(("addWord", w, None))
for i in range(0, 5000, 5):
    w = words[i]
    perf_ops.append(("search", w, True))
    perf_ops.append(("search", "." + w[1:], True))
    perf_ops.append(("search", w[:2] + "." + w[3:5] + ".", True))
    perf_ops.append(("search", w[:-1] + ("z" if w[-1] != "z" else "y") + "q", False))
cases.append(make_case(perf_ops))

# 13: single-letter words with dots
cases.append(make_case([
    ("addWord", "a", None), ("addWord", "z", None),
    ("search", "a", True), ("search", "z", True), ("search", "m", False),
    ("search", ".", True), ("search", "a.", False),
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
            if len(ops) > 40:
                bad = [i for i, (g, e) in enumerate(zip(got, exp)) if g != e]
                desc = f"{len(ops)} ops, first mismatch at op index {bad[0] if bad else '?'} ({ops[bad[0]]}{args[bad[0]]})" if bad else f"{len(ops)} ops"
                print(f"FAIL case {n}: input={desc}, expected={exp[bad[0]] if bad else exp}, got={got[bad[0]] if bad else got}")
            else:
                print(f"FAIL case {n}: input={list(zip(ops, args))}, expected={exp}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={len(ops)} ops, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)