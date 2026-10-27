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


def reference(n):
    # DP by closure number, independent of the backtracking approach
    dp = [[""]]
    for i in range(1, n + 1):
        cur = []
        for j in range(i):
            for a in dp[j]:
                for b in dp[i - 1 - j]:
                    cur.append("(" + a + ")" + b)
        dp.append(cur)
    return dp[n]


def is_valid(s, n):
    if len(s) != 2 * n:
        return False
    bal = 0
    for c in s:
        if c == "(":
            bal += 1
        elif c == ")":
            bal -= 1
        else:
            return False
        if bal < 0:
            return False
    return bal == 0


def short(x, limit=300):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "...(truncated)"


cases = [
    (3, ["((()))", "(()())", "(())()", "()(())", "()()()"]),  # example 1
    (1, ["()"]),  # example 2 / minimum
    (2, ["(())", "()()"]),
    (4, reference(4)),
    (5, reference(5)),
    (6, reference(6)),
    (7, reference(7)),
    (8, reference(8)),  # maximum, 1430 results
]
# extra: the same n called repeatedly must not leak state between calls
cases.append((3, ["((()))", "(()())", "(())()", "()(())", "()()()"]))
cases.append((1, ["()"]))

passed = 0
total = len(cases) + 1

for idx, (n, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().generateParenthesis(n)
        got_c = sorted(got)
        exp_c = sorted(expected)
        if got_c == exp_c:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={n}, expected={short(exp_c)}, got={short(got_c)}")
    except Exception as e:
        print(f"FAIL case {idx}: input={n}, error={type(e).__name__}: {e}")

# validity / uniqueness / count check for every n in the constraint range
idx = len(cases) + 1
try:
    catalan = [1, 1, 2, 5, 14, 42, 132, 429, 1430]
    problems = []
    sol = ns["Solution"]()
    for n in range(1, 9):
        got = sol.generateParenthesis(n)
        if len(got) != catalan[n]:
            problems.append(f"n={n}: count {len(got)} != {catalan[n]}")
        if len(set(got)) != len(got):
            problems.append(f"n={n}: duplicates present")
        bad = [s for s in got if not is_valid(s, n)]
        if bad:
            problems.append(f"n={n}: invalid strings e.g. {bad[:3]}")
    if not problems:
        print(f"PASS case {idx}")
        passed += 1
    else:
        print(f"FAIL case {idx}: input=n in 1..8, expected=valid unique Catalan-count strings, got={short(problems)}")
except Exception as e:
    print(f"FAIL case {idx}: input=n in 1..8, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)