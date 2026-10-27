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
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

CodecClass = ns.get("Codec") or ns.get("Solution")


def roundtrip(strs):
    # Use separate instances for encode and decode: the codec must be stateless.
    encoded = CodecClass().encode(list(strs))
    if not isinstance(encoded, str):
        raise TypeError("encode must return a str, got %s" % type(encoded).__name__)
    return CodecClass().decode(encoded)


all_ascii = "".join(chr(i) for i in range(256))

cases = [
    ["neet", "code", "love", "you"],
    ["we", "say", ":", "yes", "#4#"],
    ["", ""],
    [],
    [""],
    ["a"],
    ["#"],
    ["3#abc", "10#", "#", "##", "0#"],
    [",", " ", "  ", ";", ":", "/", "\\", "\n", "\t"],
    ["12345", "0", "007", "4#4#4#4#"],
    [all_ascii, "", all_ascii[::-1]],
    ["", "x", "", "y", ""] * 40,
    ["a" * 200 for _ in range(200)],
    ["#" * 200 if i % 2 else str(i) + "#" * (i % 50) for i in range(200)],
]

passed = 0
total = len(cases)

for n, strs in enumerate(cases, 1):
    shown = repr(strs) if len(repr(strs)) <= 200 else repr(strs)[:200] + "..."
    try:
        got = roundtrip(strs)
        if got == strs:
            print("PASS case %d" % n)
            passed += 1
        else:
            gshown = repr(got) if len(repr(got)) <= 200 else repr(got)[:200] + "..."
            print("FAIL case %d: input=%s, expected=%s, got=%s" % (n, shown, shown, gshown))
    except Exception as e:
        print("FAIL case %d: input=%s, expected=%s, got=%s: %s" % (n, shown, shown, type(e).__name__, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)