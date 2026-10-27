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


def ref(s, k):
    """Independent reference: per-letter windows."""
    best = 0
    for ch in set(s):
        l = 0
        other = 0
        for r in range(len(s)):
            if s[r] != ch:
                other += 1
            while other > k:
                if s[l] != ch:
                    other -= 1
                l += 1
            best = max(best, r - l + 1)
    return best


def random_batch():
    rng = random.Random(12345)
    cases = []
    for _ in range(300):
        n = rng.randint(1, 15)
        alpha = "ABCDE"[: rng.randint(1, 5)]
        s = "".join(rng.choice(alpha) for _ in range(n))
        k = rng.randint(0, n)
        cases.append((s, k))
    return cases


def run_random(sol):
    for s, k in random_batch():
        exp = ref(s, k)
        got = sol.characterReplacement(s, k)
        if got != exp:
            return False, (s, k), exp, got
    return True, None, None, None


rng = random.Random(7)
big_random = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(100000))

cases = [
    ("ABAB", 2, 4),
    ("AABABBA", 1, 4),
    ("A", 0, 1),
    ("A", 1, 1),
    ("AAAA", 0, 4),
    ("ABCD", 0, 1),
    ("ABCD", 4, 4),
    ("ABCDE", 2, 3),
    ("AAAAB", 1, 5),
    ("ABABABAB", 3, 7),
    ("AAAAAAAAAABBBBBBBBBB", 0, 10),
    ("A" * 100000, 0, 100000),
    ("AB" * 50000, 1000, ref("AB" * 50000, 1000)),
    (big_random, 5000, ref(big_random, 5000)),
]

passed = 0
total = len(cases) + 1
sol = ns["Solution"]()

for i, (s, k, exp) in enumerate(cases, 1):
    shown = s if len(s) <= 40 else s[:20] + "...(len=%d)" % len(s)
    try:
        got = sol.characterReplacement(s, k)
        if got == exp:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=({shown!r}, {k}), expected={exp}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input=({shown!r}, {k}), error={type(e).__name__}: {e}")

i = total
try:
    ok, inp, exp, got = run_random(sol)
    if ok:
        print(f"PASS case {i}")
        passed += 1
    else:
        print(f"FAIL case {i}: input={inp}, expected={exp}, got={got}")
except Exception as e:
    print(f"FAIL case {i}: input=random batch, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)