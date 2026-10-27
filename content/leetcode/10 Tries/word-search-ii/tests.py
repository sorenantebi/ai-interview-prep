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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def brute(board, words):
    R, C = len(board), len(board[0])

    def search(word):
        def go(r, c, i, seen):
            if board[r][c] != word[i]:
                return False
            if i == len(word) - 1:
                return True
            seen.add((r, c))
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen:
                    if go(nr, nc, i + 1, seen):
                        seen.discard((r, c))
                        return True
            seen.discard((r, c))
            return False

        return any(go(r, c, 0, set()) for r in range(R) for c in range(C))

    return sorted(w for w in words if search(w))


def grid(rows):
    return [list(r) for r in rows]


cases = []

# Examples
cases.append((grid(["oaan", "etae", "ihkr", "iflv"]), ["oath", "pea", "eat", "rain"], ["eat", "oath"]))
cases.append((grid(["ab", "cd"]), ["abcb"], []))

# Edge cases with hand-verified expectations
cases.append((grid(["a"]), ["a"], ["a"]))
cases.append((grid(["a"]), ["b"], []))
cases.append((grid(["a"]), ["aa"], []))
cases.append((grid(["ab", "cd"]), ["ab", "ac", "bd", "cd", "ad", "bc"], ["ab", "ac", "bd", "cd"]))
cases.append((grid(["abc", "def"]), ["xyz", "ad", "afd", "be"], ["ad", "be"]))
cases.append((grid(["aaaa", "aaaa"]), ["aaaaaaaa", "aaaaaaaaa"], ["aaaaaaaa"]))
cases.append((grid(["abcde"]), ["abc", "edc", "ace", "cba"], ["abc", "cba", "edc"]))
cases.append((grid(["ab"]), ["aba"], []))  # cell reuse not allowed
cases.append((grid(["a", "b", "c"]), ["abc", "cb", "ac"], ["abc", "cb"]))  # vertical, prefix words

# Random cases checked against brute force
rng = random.Random(7)
b = [[rng.choice("abc") for _ in range(4)] for _ in range(4)]
ws = list({"".join(rng.choice("abc") for _ in range(rng.randint(1, 6))) for _ in range(60)})
cases.append((b, ws, brute(b, ws)))

# Larger input for performance
b = [[rng.choice("ab") for _ in range(12)] for _ in range(12)]
ws = list({"".join(rng.choice("ab") for _ in range(10)) for _ in range(3000)})
cases.append((b, ws, brute(b, ws)))

passed = 0
total = len(cases)
for i, (board, words, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().findWords([row[:] for row in board], list(words))
        got_c = sorted(got)
        if got_c == sorted(expected):
            print(f"PASS case {i}")
            passed += 1
        else:
            show = words if len(words) <= 10 else f"<{len(words)} words>"
            print(f"FAIL case {i}: input=board={board if len(board) <= 4 else '<big>'}, words={show}, expected={sorted(expected)}, got={got_c}")
    except Exception as e:
        print(f"FAIL case {i}: input=board=..., words=..., error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)