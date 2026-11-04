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


def valid_sentences(s, words, got, expected_count):
    ws = set(words)
    if len(got) != expected_count or len(set(got)) != expected_count:
        return False
    for sent in got:
        parts = sent.split(" ")
        if "".join(parts) != s or any(p not in ws for p in parts):
            return False
    return True


# (s, wordDict, expected sorted list, or int count for validity-only check)
CASES = [
    ("catsanddog", ["cat", "cats", "and", "sand", "dog"], ["cat sand dog", "cats and dog"]),
    ("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"],
     ["pine apple pen apple", "pine applepen apple", "pineapple pen apple"]),
    ("catsandog", ["cats", "dog", "sand", "and", "cat"], []),
    ("a", ["a"], ["a"]),
    ("a", ["b"], []),
    ("aaa", ["a", "aa", "aaa"], ["a a a", "a aa", "aa a", "aaa"]),
    ("abc", ["abc"], ["abc"]),
    ("leetcode", ["leet", "code", "leetcode", "le", "et"],
     ["le et code", "leet code", "leetcode"]),
    ("ab", ["abc", "a", "b"], ["a b"]),
    ("aaaaaaaaaa", ["a", "aa", "aaa"], 274),
    ("a" * 20, ["a", "aa"], 10946),
    ("a" * 19 + "b", ["a", "aa"], []),
]


def run():
    passed = 0
    total = len(CASES)
    for i, (s, words, expected) in enumerate(CASES, 1):
        try:
            got = ns["Solution"]().wordBreak(s, list(words))
            if isinstance(expected, int):
                ok = valid_sentences(s, words, got, expected)
                exp_repr = f"{expected} valid distinct sentences"
                got_repr = f"{len(got)} sentences" if len(got) > 20 else got
            else:
                ok = sorted(got) == expected
                exp_repr = expected
                got_repr = got
            if ok:
                print(f"PASS case {i}")
                passed += 1
            else:
                print(f"FAIL case {i}: input={(s, words)}, expected={exp_repr}, got={got_repr}")
        except Exception as e:
            print(f"FAIL case {i}: input={(s, words)}, error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()