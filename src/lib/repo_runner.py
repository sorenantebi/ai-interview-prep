"""Runs a repo problem's tests without pytest: every test_* function in tests/test_*.py (Run), plus hidden_tests.py (Submit).

Usage: python repo_runner.py (Submit puts hidden_tests.py next to it, Run doesn't). Prints one line per visible test, the hidden ones only as a count and the first
failure (like LeetCode's Submit), then "N/M passed". Exits 1 when anything fails.
"""
import glob
import importlib.util
import os
import sys
import time
import traceback

sys.path.insert(0, os.getcwd())  # the repo root, so tests can `import inventory.models` etc.
sys.dont_write_bytecode = True


def load(path):
    name = os.path.splitext(path)[0].replace(os.sep, ".")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def where(e):
    """The deepest frame in the repo's own code, so the message points at a file and line."""
    frames = [f for f in traceback.extract_tb(e.__traceback__) if os.getcwd() in os.path.abspath(f.filename) and "repo_runner" not in f.filename]
    f = frames[-1] if frames else None
    return f" ({os.path.relpath(f.filename)}:{f.lineno})" if f else ""


def run(path):
    try:
        mod = load(path)
    except Exception as e:
        return [(path, False, f"{type(e).__name__} while importing: {e}{where(e)}")]
    out = []
    for name in sorted(n for n in dir(mod) if n.startswith("test_") and callable(getattr(mod, n))):
        start = time.perf_counter()
        try:
            getattr(mod, name)()
            out.append((name, True, f"{time.perf_counter() - start:.2f}s"))
        except AssertionError as e:
            out.append((name, False, f"AssertionError: {e}{where(e)}" if str(e) else f"assertion failed{where(e)}"))
        except Exception as e:
            out.append((name, False, f"{type(e).__name__}: {e}{where(e)}"))
    return out


results = []
for path in sorted(glob.glob(os.path.join("tests", "test_*.py"))):
    for name, ok, info in run(path):
        results.append((name, ok))
        print(f"{'PASS' if ok else 'FAIL'} {os.path.basename(path)}::{name}" + ("" if ok else f"\n     {info}"))
if os.path.exists("hidden_tests.py"):
    hid = run("hidden_tests.py")
    results += [(n, ok) for n, ok, _ in hid]
    passed = sum(ok for _, ok, _ in hid)
    print(f"\nHidden tests: {passed}/{len(hid)} passed")
    first = next(((n, info) for n, ok, info in hid if not ok), None)
    if first:
        print(f"First failure: {first[0].removeprefix('test_').replace('_', ' ')}\n     {first[1]}")
passed = sum(ok for _, ok in results)
print(f"\n{passed}/{len(results)} passed")
sys.exit(0 if results and passed == len(results) else 1)
