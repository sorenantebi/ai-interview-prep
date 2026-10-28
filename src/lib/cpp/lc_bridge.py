# Runs a C++ LeetCode answer (attempt.cpp) under the existing Python tests and Run comparisons.
# On import: reads the class/method signatures from starter.cpp, generates main.cpp (a JSON-lines loop that builds
# your objects and calls their methods), compiles it with attempt.cpp, and defines Python classes with the same names
# whose methods forward each call to that process. attempt.py is then just:
#     import lc_bridge; lc_bridge.bind(globals()); from lc_bridge import *
# Arguments and results cross as JSON, typed by the C++ signature (vector, string, ListNode*, TreeNode*, ...).
import hashlib, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CXX = os.environ.get("CXX") or ("g++" if os.name == "nt" else "c++")


class CompileError(Exception):
    pass


class Unsupported(Exception):
    pass


def strip_comments(src):
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", src, flags=re.S)


def split_top(s, sep=","):
    """Splits on `sep` outside <...> and (...)."""
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "<(":
            depth += 1
        elif ch in ">)":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return out


def base_type(t):
    """'const vector<int>&' -> 'vector<int>' (pointers kept)."""
    t = re.sub(r"\bconst\b|&", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s*([<>,*])\s*", r"\1", t)
    return t.replace(">>", "> >").replace("> >", ">>")


def parse_type(t):
    """'vector<pair<int,int>>' -> ('vector', [('pair', ['int', 'int'])]); leaves are plain strings."""
    m = re.match(r"^(\w+)<(.*)>$", t)
    if not m:
        return t
    return (m.group(1), [parse_type(x.strip()) for x in split_top(m.group(2))])


def parse_signatures(src):
    """{class: {"__init__": [params], method: (return type, [params])}} from LeetCode's C++ starter."""
    src = strip_comments(src)
    classes = {}
    for cm in re.finditer(r"\bclass\s+(\w+)\s*\{", src):
        name, i, depth = cm.group(1), cm.end(), 1
        start = i
        while depth and i < len(src):
            depth += {"{": 1, "}": -1}.get(src[i], 0)
            i += 1
        body = src[start:i - 1]
        # Only the top level of the class body: drop the method bodies.
        flat, depth = "", 0
        for ch in body:
            if ch == "}":
                depth -= 1
                if depth == 0:
                    flat += ";"
                continue
            if depth == 0:
                flat += ch
            if ch == "{":
                depth += 1
        methods = {}
        for sig in re.finditer(r"(?:^|[;:])\s*([\w:<>,\s\*&]*?)\s*\b(\w+)\s*\(([^()]*)\)\s*(?:const\s*)?\{", flat):
            ret, mname, params = sig.group(1).strip(), sig.group(2), sig.group(3)
            ret = re.sub(r"\b(public|private|protected|virtual|static|inline)\b\s*:?", "", ret).strip()
            plist = []
            for p in split_top(params):
                p = p.split("=")[0].strip()
                pm = re.match(r"^(.*?)(\w+)\s*$", p)
                if pm and pm.group(1).strip():
                    raw = pm.group(1).strip()
                    plist.append({"type": base_type(raw), "mutable": "&" in raw and "const" not in raw or "*" in raw})
            if mname == name and not ret:
                methods["__init__"] = plist
            elif ret and not mname.startswith("~"):
                methods[mname] = (base_type(ret), plist)
        classes[name] = methods
    return classes


def gen_main(classes):
    L = ['#include "lc_prelude.h"', '#include "attempt.cpp"', "int main(int argc, char** argv) {",
         "  FILE* proto = fdopen(atoi(argv[1]), \"w\");", "  string line;"]
    for c in classes:
        L.append(f"  unordered_map<long long, {c}*> objs_{c};")
    L += ["  while (getline(cin, line)) {", "    string out;", "    try {", "      size_t p = 0;", "      lc::J req = lc::parse(line, p);",
          "      long long id = req.a[0].i; const string& cls = req.a[1].s; const string& m = req.a[2].s; const lc::J& A = req.a[3];",
          "      TreeNode* tree = nullptr; (void)tree;", "      lc::origin.clear();"]
    for c, methods in classes.items():
        L.append(f'      if (cls == "{c}") {{')

        def args(params):
            decl, names = [], []
            for k, p in enumerate(params):
                decl.append(f"        lc::cur_arg = {k}; lc::cur_index = 0; auto a{k} = lc::arg<{p['type']}>(A.a[{k}], tree);")
                if p["type"] == "TreeNode*":
                    decl.append(f"        if (!tree) tree = a{k};")
                names.append(f"a{k}")
            return decl, ", ".join(names)

        decl, names = args(methods.get("__init__", []))
        L += ['       if (m == "") {', *decl, f"        objs_{c}[id] = new {c}({names});", '        out = "{\\"r\\":null}";', "       }"]
        for mname, sig in methods.items():
            if mname == "__init__":
                continue
            ret, params = sig
            decl, names = args(params)
            L += [f'       else if (m == "{mname}") {{', *decl, f"        auto& self = *objs_{c}.at(id);"]
            if ret == "void":
                echo = " + \",\" + ".join(f"lc::json(a{k})" for k in range(len(params))) or "string()"
                L += [f"        self.{mname}({names});", f'        out = "{{\\"r\\":null,\\"m\\":[" + {echo} + "]}}";']
            else:
                L += [f"        auto r = self.{mname}({names});", '        out = "{\\"r\\":" + lc::json(r) + "}";']
            L.append("       }")
        L.append("      }")
    L += ["    } catch (const exception& e) {", '      out = "{\\"e\\":"; lc::quote(string(typeid(e).name()) + ": " + e.what(), out); out += "}";', "    }",
          "    cout.flush();", "    fputs(out.c_str(), proto); fputc('\\n', proto); fflush(proto);", "  }", "}"]
    return "\n".join(L) + "\n"


def compile_attempt():
    starter = open("starter.cpp").read()
    if re.search(r"\bNode\s*\*", strip_comments(starter)):
        raise Unsupported("C++ isn't available for this problem yet (it uses a custom Node type). Use Python here.")
    classes = parse_signatures(starter)
    if not classes:
        raise Unsupported("Couldn't read the C++ starter's class.")
    attempt = open("attempt.cpp").read()
    code = strip_comments(attempt)
    flags = [f"-DLC_OWN_{t.upper()}" for t in ("ListNode", "TreeNode") if re.search(rf"\bstruct\s+{t}\s*\{{", code)]
    with open("main.cpp", "w") as f:
        f.write(gen_main(classes))
    prelude = open(os.path.join(HERE, "lc_prelude.h")).read()  # next to this file (run.ts copies both)
    key = hashlib.sha1((attempt + starter + prelude + " ".join(flags)).encode()).hexdigest()[:12]
    binary = os.path.join(tempfile.gettempdir(), f"prep-lc-{key}" + (".exe" if os.name == "nt" else ""))
    # shortcut: compiled answers pile up in the temp dir until the OS clears it; prune old prep-lc-* files if that ever matters.
    if not os.path.exists(binary):  # cached: Run and Submit on unchanged code compile once
        r = subprocess.run([CXX, "-std=c++20", "-O2", "-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST", *flags, "-o", binary, "main.cpp"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            msg = "\n".join(l for l in r.stderr.splitlines() if "main.cpp" not in l or "error" in l)
            raise CompileError(re.sub(r"(?m)^(\./)?attempt\.cpp:", "line ", msg)[:3000])
    return classes, binary


# ---- Python side -------------------------------------------------------------------------------------------------

_ns = {}


def bind(ns):
    """The namespace the tests exec attempt.py in: its ListNode / TreeNode classes are used for results."""
    _ns["ns"] = ns


class _Node:
    def __init__(self, val=0, next=None, left=None, right=None):
        self.val, self.next, self.left, self.right = val, next, left, right


def _cls(name):
    return _ns.get("ns", {}).get(name) or _Node


_inputs = {}  # this call's input list nodes: argument index -> [nodes]


def list_in(head, arg=0):
    vals, seen, nodes, n = [], {}, [], head
    while n is not None and id(n) not in seen:
        seen[id(n)] = len(vals)
        vals.append(n.val)
        nodes.append(n)
        n = n.next
    _inputs.setdefault(arg, []).extend(nodes)
    return {"vals": vals, "pos": seen[id(n)]} if n is not None else vals


def tree_in(root):
    out, queue = [], [root]
    for n in queue:
        out.append(None if n is None else n.val)
        if n is not None:
            queue += [n.left, n.right]
    while out and out[-1] is None:
        out.pop()
    return out


def contains(root, node):
    stack = [root]
    while stack:
        n = stack.pop()
        if n is node:
            return True
        if n is not None:
            stack += [n.left, n.right]
    return False


def to_json(t, x, tree=None, arg=0):
    if x is None:
        return None
    if t == "ListNode*":
        return list_in(x, arg)
    if t == "TreeNode*":
        return {"node": x.val} if tree is not None and contains(tree, x) else tree_in(x)
    if isinstance(t, tuple) and isinstance(x, (list, tuple)):
        inner = t[1]
        return [to_json(inner[0] if t[0] == "vector" else inner[k], v, None, arg) for k, v in enumerate(x)]
    return x


def build_list(vals):
    if isinstance(vals, dict):  # reuses the caller's nodes where C++ returned them
        nodes = [_inputs[i[0]][i[1]] if i is not None else _cls("ListNode")(v) for v, i in zip(vals["vals"], vals["ids"])]
        for node, v in zip(nodes, vals["vals"]):
            node.val = v
        for a, b in zip(nodes, nodes[1:]):
            a.next = b
        if nodes:
            nodes[-1].next = None
        return nodes[0] if nodes else None
    head = None
    for v in reversed(vals):
        head = _cls("ListNode")(v, head) if _cls("ListNode") is not _Node else _Node(v, head)
    return head


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    T = _cls("TreeNode")
    root = T(vals[0])
    queue, i = [root], 1
    for n in queue:
        if i >= len(vals):
            break
        for side in ("left", "right"):
            if i < len(vals) and vals[i] is not None:
                setattr(n, side, T(vals[i]))
                queue.append(getattr(n, side))
            i += 1
    return root


def from_json(t, v):
    if v is None:
        return None
    if t == "ListNode*":
        return build_list(v)
    if t == "TreeNode*":
        return build_tree(v)
    if isinstance(t, tuple) and isinstance(v, list):
        inner = t[1]
        return [from_json(inner[0] if t[0] == "vector" else inner[k], x) for k, x in enumerate(v)]
    return v


def write_back(t, py, v):
    """In-place problems (void methods): copy the C++ result back into the Python argument object (rows too)."""
    if isinstance(py, list) and isinstance(v, list):
        inner = t[1][0] if isinstance(t, tuple) and t[0] == "vector" else None
        if len(py) == len(v) and all(isinstance(r, list) for r in py):
            for row, new in zip(py, v):
                write_back(inner, row, new)
        else:
            py[:] = from_json(t, v)
    elif t == "ListNode*" and py is not None and isinstance(v, dict):
        build_list(v)  # relinks the caller's nodes
    elif t == "ListNode*" and py is not None and isinstance(v, list):
        nodes, n = [], py
        while n is not None and len(nodes) < len(v):
            nodes.append(n)
            n = n.next
        for node, val in zip(nodes, v):
            node.val = val
        if nodes:  # relink in order and cut any leftover tail
            for a, b in zip(nodes, nodes[1:]):
                a.next = b
            nodes[-1].next = None


class _Process:
    def __init__(self, binary):
        self.binary, self.proc, self.gen, self.next_id = binary, None, 0, 0
        self.out_path = os.path.join(tempfile.gettempdir(), f"prep-lc-out-{os.getpid()}.txt")

    def start(self):
        r, w = os.pipe()
        self.out = open(self.out_path, "w+")
        kw = {"pass_fds": (w,)} if os.name != "nt" else {}
        # UTF-8 both ways; a C++ answer that splits a multi-byte character comes back with a replacement character.
        self.proc = subprocess.Popen([self.binary, str(w)], stdin=subprocess.PIPE, stdout=self.out, text=True, encoding="utf-8", **kw)
        os.close(w)
        self.proto = os.fdopen(r, encoding="utf-8", errors="replace")
        self.gen += 1

    def call(self, obj_id, cls, method, args):
        if self.proc is None or self.proc.poll() is not None:
            self.start()
        self.proc.stdin.write(json.dumps([obj_id, cls, method, args], separators=(",", ":")) + "\n")
        self.proc.stdin.flush()
        line = self.proto.readline()
        self.out.seek(0)
        printed = self.out.read()
        if printed:  # your cout output, shown as Stdout
            sys.stdout.write(printed)
            self.out.seek(0)
            self.out.truncate()
        if not line:
            code = self.proc.wait()
            self.proc = None
            sig = f" (signal {-code})" if code < 0 else f" (exit code {code})"
            raise RuntimeError("Your C++ code crashed" + sig + ": a null or dangling pointer, out-of-range access or stack overflow?")
        res = json.loads(line)
        if "e" in res:
            raise RuntimeError(res["e"])
        return res


def _make_class(name, methods, proc):
    def init(self, *a):
        proc.next_id += 1
        self._id, self._gen = proc.next_id, None
        params = methods.get("__init__", [])
        proc.call(self._id, name, "", [to_json(parse_type(p["type"]), x) for p, x in zip(params, a)])
        self._gen = proc.gen

    def method(mname, ret, params):
        def call(self, *a):
            if self._gen != proc.gen:
                raise RuntimeError("This object was lost when your C++ code crashed earlier.")
            tree, sent = None, []
            _inputs.clear()
            for k, (p, x) in enumerate(zip(params, a)):
                sent.append(to_json(parse_type(p["type"]), x, tree, k))
                if p["type"] == "TreeNode*" and tree is None:
                    tree = x
            res = proc.call(self._id, name, mname, sent)
            for p, x, v in zip(params, a, res.get("m", [])):
                if p["mutable"]:
                    write_back(parse_type(p["type"]), x, v)
            return from_json(parse_type(ret), res["r"])
        call.__name__ = mname
        return call

    attrs = {"__init__": init}
    for mname, sig in methods.items():
        if mname != "__init__":
            attrs[mname] = method(mname, *sig)
    return type(name, (), attrs)


def _python_classes():
    """Class names the Python starter (and so the tests) use, e.g. Solution vs C++'s Codec."""
    try:
        return re.findall(r"^class (\w+)", open("starter.py").read(), re.M)
    except OSError:
        return []


_classes, _binary = compile_attempt()
_proc = _Process(_binary)
__all__ = []
for _name, _methods in _classes.items():
    globals()[_name] = _make_class(_name, _methods, _proc)
    __all__.append(_name)
for _name in _python_classes():  # a differently named class with the same methods stands in
    if _name not in globals():
        match = [c for c in _classes if c not in ("ListNode", "TreeNode")]
        if len(match) == 1:
            globals()[_name] = globals()[match[0]]
            __all__.append(_name)
