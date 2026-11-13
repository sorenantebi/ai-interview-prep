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


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = [root]
    i = 1
    while q and i < len(arr):
        n = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            n.left = TreeNode(arr[i])
            q.append(n.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            n.right = TreeNode(arr[i])
            q.append(n.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = [root]
    while q:
        n = q.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

big_mid = "a  " + " ".join(["a"] * 49)
big_mid = "a" + "  " + "a" + " a" * 48
assert len(big_mid) == 100
big_last = " ".join(["a"] * 50) + " "
assert len(big_last) == 100

CASES = [
    (["This", "is", "an", "example", "of", "text", "justification."], 16,
     ["This    is    an", "example  of text", "justification.  "]),
    (["What", "must", "be", "acknowledgment", "shall", "be"], 16,
     ["What   must   be", "acknowledgment  ", "shall be        "]),
    (["Science", "is", "what", "we", "understand", "well", "enough", "to", "explain",
      "to", "a", "computer.", "Art", "is", "everything", "else", "we", "do"], 20,
     ["Science  is  what we", "understand      well", "enough to explain to",
      "a  computer.  Art is", "everything  else  we", "do                  "]),
    (["a"], 1, ["a"]),
    (["hello"], 10, ["hello     "]),
    (["a", "b", "c", "d"], 1, ["a", "b", "c", "d"]),
    (["a", "b", "c"], 5, ["a b c"]),
    (["a", "b", "c", "d", "e"], 3, ["a b", "c d", "e  "]),
    (["a", "b", "c", "dd"], 7, ["a  b  c", "dd     "]),
    (["ab", "cd", "ef", "g"], 9, ["ab  cd ef", "g        "]),
    (["listen", "to", "me", "now", "ok"], 10, ["listen  to", "me now ok "]),
    (["a"] * 300, 100, [big_mid] * 5 + [big_last]),
]


def main():
    passed = 0
    total = len(CASES)
    for n, (words, width, expected) in enumerate(CASES, 1):
        try:
            got = ns["Solution"]().fullJustify(list(words), width)
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input=({words}, {width}), expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input=({words}, {width}), error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()