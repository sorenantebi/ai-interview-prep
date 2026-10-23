# Runs LeetCode-style test cases against attempt.py and the NeetCode reference (reference.py).
# Input: spec.json {"cases": [[str, ...]], "names": [...], "anyOrder": bool, "multi": bool} plus starter.py.
# Output: a JSON list of results after a "__RESULTS__" marker line.
import ast, contextlib, inspect, io, json, re, sys, traceback
import bisect, collections, functools, heapq, itertools, math, random, string  # noqa: F401  (LeetCode pre-imports)
from bisect import *  # noqa: F401,F403
from collections import *  # noqa: F401,F403
from functools import *  # noqa: F401,F403
from heapq import *  # noqa: F401,F403
from itertools import *  # noqa: F401,F403
from math import inf  # noqa: F401
from typing import *  # noqa: F401,F403

sys.setrecursionlimit(10000)


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


class GraphNode:  # Clone Graph
    def __init__(self, val=0, neighbors=None):
        self.val, self.neighbors = val, neighbors if neighbors is not None else []


class RandomNode:  # Copy List With Random Pointer
    def __init__(self, x=0, next=None, random=None):
        self.val, self.next, self.random = int(x), next, random


STARTER = open("starter.py").read()
Node = GraphNode if "neighbors" in STARTER else RandomNode


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def list_values(head, limit=10**5):
    out = []
    while head and len(out) < limit:
        out.append(head.val)
        head = head.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue, i = deque([root]), 1
    while queue and i < len(vals):
        node = queue.popleft()
        for side in ("left", "right"):
            if i < len(vals) and vals[i] is not None:
                setattr(node, side, TreeNode(vals[i]))
                queue.append(getattr(node, side))
            i += 1
    return root


def tree_values(root):
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        out.append(node.val if node else None)
        if node:
            queue.extend([node.left, node.right])
    while out and out[-1] is None:
        out.pop()
    return out


def find_val(root, val):
    stack = [root]
    while stack:
        n = stack.pop()
        if n:
            if n.val == val:
                return n
            stack += [n.left, n.right]
    return TreeNode(val)


def build_graph(adj):
    if not adj:
        return None
    nodes = [GraphNode(i + 1) for i in range(len(adj))]
    for i, nbrs in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nbrs]
    return nodes[0]


def graph_values(node):
    if not node:
        return []
    seen, queue = {node.val: node}, deque([node])
    while queue:
        for n in queue.popleft().neighbors:
            if n.val not in seen:
                seen[n.val] = n
                queue.append(n)
    return [[n.val for n in seen[v].neighbors] for v in sorted(seen)]


def build_random(pairs):
    nodes = [RandomNode(v) for v, _ in pairs]
    for i, (_, r) in enumerate(pairs):
        nodes[i].next = nodes[i + 1] if i + 1 < len(nodes) else None
        nodes[i].random = nodes[r] if r is not None else None
    return nodes[0] if nodes else None


def random_values(head):
    nodes = []
    while head and len(nodes) < 10**5:
        nodes.append(head)
        head = head.next
    index = {id(n): i for i, n in enumerate(nodes)}
    return [[n.val, index.get(id(n.random)) if n.random else None] for n in nodes]


def base_ns():
    ns = {k: v for k, v in globals().items() if not k.startswith("__")}
    ns.update(__name__="solution", Node=Node)
    return ns


def load(fname, lenient=False):
    src = open(fname).read()
    if lenient:  # NeetCode files sometimes append broken alternate versions: keep the longest prefix that compiles
        lines = src.split("\n")
        for n in range(len(lines), 0, -1):
            try:
                compile("\n".join(lines[:n]), fname, "exec")
                src = "\n".join(lines[:n])
                break
            except SyntaxError:
                continue
    ns = base_ns()
    exec(compile(src, fname, "exec"), ns)
    return ns


def entry(ns):
    """The method to call: Solution.<method>, else the class's first own public method, else a bare function."""
    cls = ns.get(main)
    if cls is not None and hasattr(cls, method):
        return getattr(cls(), method)
    if cls is not None:
        own = [v for k, v in vars(cls).items() if callable(v) and not k.startswith("_")]
        if own:
            return own[0].__get__(cls())
    fn = ns.get(method) or ns.get(re.sub(r"(?<!^)([A-Z])", r"_\1", method).lower())
    if callable(fn):
        return functools.partial(fn, None) if "self" in inspect.signature(fn).parameters else fn
    raise AttributeError(f"no {main}.{method} found")


def parse(text):
    text = text.strip()
    try:
        return json.loads(text)
    except ValueError:
        try:
            return ast.literal_eval(text)
        except (ValueError, SyntaxError):
            return json.loads(re.sub(r"\bINF\b", "2147483647", text))  # Walls and Gates writes INF


def to_out(x, by_value=False):
    if isinstance(x, ListNode):
        return list_values(x)
    if isinstance(x, TreeNode):
        return x.val if by_value else tree_values(x)
    if isinstance(x, GraphNode):
        return graph_values(x)
    if isinstance(x, RandomNode):
        return random_values(x)
    if isinstance(x, (list, tuple)):
        return [to_out(i, by_value) for i in x]
    if isinstance(x, set):
        return sorted(to_out(i) for i in x)
    return x


st = load("starter.py")
classes = re.findall(r"^class (\w+)", STARTER, re.M)
main = next((c for c in classes if c in ("Solution", "Codec")), None)
method = re.search(r"^\s+def (?!_)(\w+)\(self", STARTER, re.M).group(1) if main else None
sig = inspect.signature(getattr(st[main], method)) if main else None
anns = [str(p.annotation) for p in list(sig.parameters.values())[1:]] if sig else []
returns_none = sig is not None and sig.return_annotation in (None, "None")


def run_case(ns, values):
    """Runs one case in a namespace; returns the LeetCode-style output value."""
    if not main:  # design class: calls + args
        calls, args = values
        cls = ns[calls[0]]
        obj, out = cls(*args[0]), [None]
        for name, a in zip(calls[1:], args[1:]):
            out.append(to_out(getattr(obj, name)(*a)))
        return out
    # Round trips: serialize/deserialize, encode/decode (on whichever class defines them).
    pair = next(((a, b) for a, b in (("serialize", "deserialize"), ("encode", "decode")) if a == method), None)
    if pair:
        holder = next(v for v in ns.values() if inspect.isclass(v) and hasattr(v, pair[0]) and hasattr(v, pair[1]))
        x = build_tree(values[0]) if pair[0] == "serialize" else values[0]
        back = getattr(holder(), pair[1])(getattr(holder(), pair[0])(x))
        return tree_values(back) if pair[0] == "serialize" else to_out(back)
    args, tree, by_value = [], None, False
    for i, ann in enumerate(anns):
        v = values[i] if i < len(values) else None
        if "ListNode" in ann:
            v = [build_list(x) for x in v] if re.match(r"^(typing\.)?[Ll]ist\[", ann) else build_list(v)
        elif "TreeNode" in ann:
            if isinstance(v, int) and tree is not None:  # e.g. LCA: p = 2 means the node with value 2
                v, by_value = find_val(tree, v), True
            else:
                v = build_tree(v)
                tree = tree or v
        elif "Node" in ann:
            v = build_graph(v) if Node is GraphNode else build_random(v)
        args.append(v)
    if len(values) == len(anns) + 1 and anns and "ListNode" in anns[0] and values[-1] >= 0:  # Linked List Cycle: pos
        tail = args[0]
        while tail and tail.next:
            tail = tail.next
        target = args[0]
        for _ in range(values[-1]):
            target = target.next
        if tail:
            tail.next = target
    result = entry(ns)(*args)
    if returns_none and result is None:
        return to_out(args[0])  # in-place problems: the modified input is the answer
    if result is None and re.search(r"ListNode|TreeNode|Node", str(sig.return_annotation)):
        return None if by_value else []  # empty list / tree prints as [] on LeetCode
    return to_out(result, by_value)


def canon(x, deep):
    if isinstance(x, float):
        return round(x, 5)
    if isinstance(x, list):
        items = [canon(i, deep) if deep else canon_flat(i) for i in x]
        return sorted(items, key=lambda i: json.dumps(i, sort_keys=True))
    return x


def canon_flat(x):
    return round(x, 5) if isinstance(x, float) else [canon_flat(i) for i in x] if isinstance(x, list) else x


def fmt(x):
    """LeetCode's display format: JSON-like, floats with 5 decimals."""
    if x is None:
        return "null"
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, float):
        return f"{x:.5f}"
    if isinstance(x, (int, str)):
        return json.dumps(x)
    if isinstance(x, (list, tuple)):
        return "[" + ",".join(fmt(i) for i in x) + "]"
    return repr(x)


spec = json.load(open("spec.json"))
attempt_ns = reference_ns = None
load_error = None
try:
    attempt_ns = load("attempt.py")
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)
    line = next((f.lineno for f in reversed(tb) if f.filename == "attempt.py"), getattr(e, "lineno", None))
    load_error = f"{type(e).__name__}: {e}" + (f" (line {line})" if line else "")
try:
    reference_ns = load("reference.py", lenient=True)
except Exception:
    reference_ns = None

results = []
for raw in spec["cases"]:
    r = {"input": raw}
    try:
        values = [parse(v) for v in raw]
    except Exception as e:
        r.update(ok=False, error=f"Could not read this input: {e}")
        results.append(r)
        continue
    exp, have_exp = None, False
    if reference_ns:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exp = run_case(reference_ns, [parse(v) for v in raw])
            r["expected"], have_exp = fmt(exp), True
        except Exception as e:
            r["expected"] = f"(reference failed: {type(e).__name__}: {e})"
    if load_error:
        r.update(ok=False, error=load_error)
        results.append(r)
        continue
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            got = run_case(attempt_ns, values)
        r["output"] = fmt(got)
        if not have_exp:
            r.update(ok=None, note="no reference answer to compare with")
        elif canon_flat(got) == canon_flat(exp):
            r["ok"] = True
        elif spec.get("anyOrder") and canon(got, False) == canon(exp, False):
            r["ok"] = True
        elif spec.get("anyOrder") and canon(got, True) == canon(exp, True):
            r.update(ok=True, note="matches when order inside each group is ignored")
        elif spec.get("multi"):
            r.update(ok=None, note="differs from NeetCode's answer, but this problem accepts several answers; check yours is valid")
        else:
            r["ok"] = False
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        line = next((f.lineno for f in reversed(tb) if f.filename == "attempt.py"), None)
        r.update(ok=False, error=f"{type(e).__name__}: {e}" + (f" (line {line})" if line else ""))
    if buf.getvalue():
        r["stdout"] = buf.getvalue()[:5000]
    results.append(r)

print("__RESULTS__")
print(json.dumps(results))
