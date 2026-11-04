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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

letters = "abcdefghijklmnopqrstuvwxyz"

# 25 chained equalities a==b, b==c, ..., y==z
chain_all = [letters[i] + "==" + letters[i + 1] for i in range(25)]
# 12 chained equalities a==b, ..., l==m
chain_am = [letters[i] + "==" + letters[i + 1] for i in range(12)]

# Large unsatisfiable: whole alphabet is one group, final a!=z contradicts it
large_false = (chain_all * 20)[:499] + ["a!=z"]

# Large satisfiable: a..m are one group, z and n are outside it
large_true = chain_am * 30
while len(large_true) < 500:
    large_true.append("a!=z" if len(large_true) % 2 == 0 else "m!=n")

assert len(large_false) == 500
assert len(large_true) == 500

cases = [
    (["a==b", "b!=a"], False),
    (["b==a", "a==b"], True),
    (["a==b", "b==c", "a==c"], True),
    (["a==b", "b!=c", "c==a"], False),
    (["c==c", "b==d", "x!=z"], True),
    (["a!=a"], False),
    (["a==a"], True),
    (["a!=b"], True),
    (["a==b", "c==d", "a!=c"], True),
    (["a==b", "c==d", "b==c", "a!=d"], False),
    (["a!=b", "b==c", "c==a"], False),
    (large_false, False),
    (large_true, True),
]

passed = 0
total = len(cases)
for i, (eqs, expected) in enumerate(cases, 1):
    shown = eqs if len(eqs) <= 10 else "<%d equations>" % len(eqs)
    try:
        sol = ns["Solution"]()
        got = sol.equationsPossible(list(eqs))
        if got == expected:
            print("PASS case %d" % i)
            passed += 1
        else:
            print("FAIL case %d: input=%s, expected=%s, got=%s" % (i, shown, expected, got))
    except Exception as e:
        print("FAIL case %d: input=%s, error=%s" % (i, shown, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)
