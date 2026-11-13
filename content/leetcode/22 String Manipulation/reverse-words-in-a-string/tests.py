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

big_words = ["w%d" % i for i in range(1500)]
big_input = "  ".join(big_words)
big_input = "   " + big_input + "    "
big_expected = " ".join(reversed(big_words))

long_word = "a" * 10000

cases = [
    ("the sky is blue", "blue is sky the"),
    ("  hello world  ", "world hello"),
    ("a good   example", "example good a"),
    ("a", "a"),
    ("   a   ", "a"),
    ("hello", "hello"),
    ("A1 b2 C3", "C3 b2 A1"),
    ("  Bob    Loves  Alice   Bob  ", "Bob Alice Loves Bob"),
    ("x y z", "z y x"),
    (" 123 45", "45 123"),
    (big_input, big_expected),
    (long_word, long_word),
]


def short(v):
    r = repr(v)
    return r if len(r) <= 120 else r[:117] + "..."


passed = 0
total = len(cases)
for i, (inp, exp) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().reverseWords(inp)
        if got == exp:
            print("PASS case %d" % i)
            passed += 1
        else:
            print("FAIL case %d: input=%s, expected=%s, got=%s" % (i, short(inp), short(exp), short(got)))
    except Exception as e:
        print("FAIL case %d: input=%s, error=%s: %s" % (i, short(inp), type(e).__name__, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)
