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


def list_to_py(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

# (input string, expected compressed string)
CASES = [
    ("aabbccc", "a2b2c3"),
    ("a", "a"),
    ("a" + "b" * 12, "ab12"),
    ("abc", "abc"),
    ("aa", "a2"),
    ("a" * 10, "a10"),
    ("a" * 9, "a9"),
    ("x" * 100, "x100"),
    ("z" * 2000, "z2000"),
    ("11!!!", "12!3"),
    ("aabbaa", "a2b2a2"),
    ("abcc", "abc2"),
    ("aAAa", "aA2a"),
    ("a" * 1000 + "b" * 1000, "a1000b1000"),
]


def main():
    passed = 0
    total = len(CASES)
    for i, (inp, exp) in enumerate(CASES, 1):
        chars = list(inp)
        exp_list = list(exp)
        exp_len = len(exp_list)
        short = inp if len(inp) <= 40 else inp[:20] + "...(len %d)" % len(inp)
        try:
            sol = ns["Solution"]()
            ret = sol.compress(chars)
            got = chars[:ret] if isinstance(ret, int) and ret >= 0 else None
            if ret == exp_len and got == exp_list:
                print("PASS case %d" % i)
                passed += 1
            else:
                got_s = "".join(got) if got is not None else None
                exp_s = exp if len(exp) <= 40 else exp[:20] + "..."
                print("FAIL case %d: input=%r, expected=(%d, %r), got=(%r, %r)" % (i, short, exp_len, exp_s, ret, got_s if got_s is None or len(got_s) <= 40 else got_s[:20] + "..."))
        except Exception as e:
            print("FAIL case %d: input=%r, error=%s: %s" % (i, short, type(e).__name__, e))
    print("%d/%d passed" % (passed, total))
    if passed != total:
        sys.exit(1)


main()