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


def reference_len(s):
    best = 0
    n = len(s)
    for c in range(2 * n - 1):
        l = c // 2
        r = l + c % 2
        while l >= 0 and r < n and s[l] == s[r]:
            l -= 1
            r += 1
        best = max(best, r - l - 1)
    return best


# (input, expected length, set of accepted answers or None for any valid)
CASES = [
    ("babad", 3, {"bab", "aba"}),
    ("cbbd", 2, {"bb"}),
    ("a", 1, {"a"}),
    ("ac", 1, {"a", "c"}),
    ("aa", 2, {"aa"}),
    ("aaaa", 4, {"aaaa"}),
    ("racecar", 7, {"racecar"}),
    ("abcdefg", 1, None),
    ("forgeeksskeegfor", 10, {"geeksskeeg"}),
    ("123454321xyz", 9, {"123454321"}),
    ("a" * 1000, 1000, {"a" * 1000}),
    ("ab" * 500, 999, None),
    ("xyz" + "abcdedcba" * 1 + "q" * 2 + "0123456789" * 50, None, None),
]


def check(s, exp_len, accepted, got):
    if not isinstance(got, str):
        return False
    if exp_len is None:
        exp_len = reference_len(s)
    if len(got) != exp_len:
        return False
    if got not in s or got != got[::-1]:
        return False
    if accepted is not None and got not in accepted:
        return False
    return True


def main():
    passed = 0
    total = len(CASES)
    for i, (s, exp_len, accepted) in enumerate(CASES, 1):
        shown = s if len(s) <= 40 else s[:37] + "..."
        exp_len_val = exp_len if exp_len is not None else reference_len(s)
        expected = sorted(accepted) if accepted is not None and len(s) <= 40 else f"any palindromic substring of length {exp_len_val}"
        try:
            got = ns["Solution"]().longestPalindrome(s)
            ok = check(s, exp_len, accepted, got)
            got_show = got if not isinstance(got, str) or len(got) <= 40 else got[:37] + "..."
        except Exception as e:
            ok = False
            got_show = f"{type(e).__name__}: {e}"
        if ok:
            passed += 1
            print(f"PASS case {i}")
        else:
            print(f"FAIL case {i}: input={shown!r}, expected={expected}, got={got_show!r}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()