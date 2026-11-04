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

CASES = [
    (["flower", "flow", "flight"], "fl"),
    (["dog", "racecar", "car"], ""),
    (["a"], "a"),
    ([""], ""),
    (["", "abc"], ""),
    (["abc", ""], ""),
    (["abc", "abc", "abc"], "abc"),
    (["abc", "ab", "abcd"], "ab"),
    (["ab", "abc"], "ab"),
    (["a", "b"], ""),
    (["interview", "internet", "interval", "internal"], "inter"),
    (["a" * 200] * 200, "a" * 200),
    (["a" * 150 + "b" * 50, "a" * 150 + "c" * 50] + ["a" * 150 + "b" * 50] * 198, "a" * 150),
]


def main():
    passed = 0
    for n, (strs, expected) in enumerate(CASES, 1):
        arg = list(strs)
        try:
            got = ns["Solution"]().longestCommonPrefix(arg)
            ok = got == expected
        except Exception as e:
            ok = False
            got = f"{type(e).__name__}: {e}"
        shown = strs if len(str(strs)) < 100 else f"<{len(strs)} strings, first len {len(strs[0])}>"
        if ok:
            passed += 1
            print(f"PASS case {n}")
        else:
            exp = expected if len(expected) < 50 else f"<{len(expected)} chars>"
            g = got if len(str(got)) < 50 else f"<{len(str(got))} chars>"
            print(f"FAIL case {n}: input={shown}, expected={exp!r}, got={g!r}")
    print(f"{passed}/{len(CASES)} passed")
    if passed != len(CASES):
        sys.exit(1)


main()