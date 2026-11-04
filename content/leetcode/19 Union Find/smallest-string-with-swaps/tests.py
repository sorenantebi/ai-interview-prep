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

N = 100000
big_s = "".join(chr(97 + (i * 7) % 26) for i in range(N))
big_chain = [[i, i + 1] for i in range(N - 1)]
big_chain_rev = [[i + 1, i] for i in range(N - 2, -1, -1)]

# evens chained only; odd positions stay untouched
even_pairs = [[i, i + 2] for i in range(0, N - 2, 2)]
even_sorted = sorted(big_s[0::2])
even_expected = [""] * N
even_expected[0::2] = even_sorted
even_expected[1::2] = list(big_s[1::2])
even_expected = "".join(even_expected)

cases = [
    ("dcab", [[0, 3], [1, 2]], "bacd"),
    ("dcab", [[0, 3], [1, 2], [0, 2]], "abcd"),
    ("cba", [[0, 1], [1, 2]], "abc"),
    ("a", [], "a"),
    ("zyx", [], "zyx"),
    ("ba", [[0, 0]], "ba"),
    ("dcba", [[0, 1], [0, 1], [1, 0]], "cdba"),
    ("bca", [[0, 2]], "acb"),
    ("edcba", [[0, 4], [1, 3]], "abcde"),
    ("bbaa", [[0, 3]], "abab"),
    (big_s, big_chain, "".join(sorted(big_s))),
    (big_s, big_chain_rev, "".join(sorted(big_s))),
    (big_s, even_pairs, even_expected),
]


def short(x):
    r = repr(x)
    return r if len(r) <= 80 else r[:77] + "..."


passed = 0
total = len(cases)
for i, (s, pairs, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().smallestStringWithSwaps(s, [list(p) for p in pairs])
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=({short(s)}, {short(pairs)}), expected={short(expected)}, got={short(got)}")
    except BaseException as e:
        print(f"FAIL case {i}: input=({short(s)}, {short(pairs)}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
