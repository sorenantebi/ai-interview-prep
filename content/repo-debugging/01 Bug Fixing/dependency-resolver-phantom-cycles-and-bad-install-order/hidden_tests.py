import random

from pkgres import (
    CycleError,
    MissingPackage,
    Registry,
    Resolver,
    VersionConflict,
    build_plan,
)
from pkgres.versions import parse_version, satisfies


def _raises(exc_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exc_type as exc:
        return exc
    raise AssertionError(f"{exc_type.__name__} not raised")


def _random_dag(n):
    rng = random.Random(0)
    deps = {}
    for i in range(n):
        count = min(i, rng.randint(0, 4))
        deps[i] = sorted(rng.sample(range(i), count))
    mapping = {
        f"p{i}": ("1.0", [f"p{j}>=1.0" for j in deps[i]]) for i in range(n)
    }
    return deps, Registry.from_mapping(mapping)


def test_cycle_chain_excludes_unrelated_prefix():
    registry = Registry.from_mapping({
        "app": ("1.0", ["a"]),
        "a": ("1.0", ["b"]),
        "b": ("1.0", ["a"]),
    })
    exc = _raises(CycleError, Resolver(registry).resolve, ["app"])
    assert exc.chain == ["a", "b", "a"]


def test_self_dependency_is_a_cycle():
    registry = Registry.from_mapping({"a": ("1.0", ["a"])})
    exc = _raises(CycleError, Resolver(registry).resolve, ["a"])
    assert exc.chain == ["a", "a"]


def test_cycle_found_behind_a_shared_dependency():
    registry = Registry.from_mapping({
        "app": ("1.0", ["x", "y"]),
        "x": ("1.0", ["base"]),
        "base": ("1.0", []),
        "y": ("1.0", ["base", "z"]),
        "z": ("1.0", ["y"]),
    })
    exc = _raises(CycleError, Resolver(registry).resolve, ["app"])
    assert exc.chain == ["y", "z", "y"]


def test_empty_request():
    registry = Registry.from_mapping({"a": ("1.0", [])})
    assert Resolver(registry).resolve([]) == []
    assert build_plan(registry, []).stages == []


def test_declaration_order_is_kept():
    registry = Registry.from_mapping({
        "app": ("1.0", ["b", "a"]),
        "a": ("1.0", []),
        "b": ("1.0", []),
    })
    assert Resolver(registry).resolve(["app"]) == ["b", "a", "app"]


def test_root_listed_twice_or_also_a_dependency():
    registry = Registry.from_mapping({
        "app": ("1.0", ["lib"]),
        "lib": ("1.0", []),
    })
    resolver = Resolver(registry)
    assert resolver.resolve(["app", "app"]) == ["lib", "app"]
    assert resolver.resolve(["lib", "app"]) == ["lib", "app"]


def test_conflicting_constraints_on_shared_dependency():
    registry = Registry.from_mapping({
        "app": ("1.0", ["left", "right"]),
        "left": ("1.0", ["base>=1.0"]),
        "right": ("1.0", ["base>=3.0"]),
        "base": ("2.0", []),
    })
    exc = _raises(VersionConflict, Resolver(registry).resolve, ["app"])
    assert exc.required_by == "right"
    assert exc.found == "2.0"


def test_missing_transitive_dependency_reports_parent():
    registry = Registry.from_mapping({
        "app": ("1.0", ["lib"]),
        "lib": ("1.0", ["ghost"]),
    })
    exc = _raises(MissingPackage, Resolver(registry).resolve, ["app"])
    assert exc.name == "ghost"
    assert exc.required_by == "lib"


def test_names_are_case_insensitive():
    registry = Registry.from_mapping({
        "App": ("1.0", ["LibA", "liba"]),
        "LIBA": ("1.0", []),
    })
    assert Resolver(registry).resolve(["app"]) == ["liba", "app"]


def test_parse_version_rejects_garbage():
    for text in ["", "1..2", "a.b", "1.x", "-1"]:
        _raises(ValueError, parse_version, text)


def test_version_ordering_across_digit_counts():
    assert parse_version("1.2.10") > parse_version("1.2.9")
    assert parse_version("10.0") > parse_version("9.9.9")
    assert parse_version("1.0") == parse_version("1.0.0")
    assert parse_version("0.0") == parse_version("0")


def test_strict_and_inclusive_bounds():
    assert satisfies("2.0", ">1.10")
    assert not satisfies("1.10", ">1.10")
    assert satisfies("1.10", ">=1.10")
    assert satisfies("1.9", "<1.10")
    assert not satisfies("1.10", "<1.10")
    assert satisfies("1.10", "<=1.10.0")
    assert satisfies("3.1", "")


def test_two_digit_component_in_range():
    assert satisfies("1.12.3", ">=1.9,<1.20")
    assert not satisfies("1.20.0", ">=1.9,<1.20")


def test_plan_flat_order_is_dependency_first():
    registry = Registry.from_mapping({
        "app": ("1.0", ["lib", "tool"]),
        "lib": ("1.0", ["core"]),
        "tool": ("1.0", []),
        "core": ("1.0", []),
    })
    plan = build_plan(registry, ["app"])
    assert plan.order == ["core", "tool", "lib", "app"]


def test_plan_with_shared_dependency_at_different_depths():
    registry = Registry.from_mapping({
        "app": ("1.0", ["lib", "core"]),
        "lib": ("1.0", ["core"]),
        "core": ("1.0", []),
    })
    assert build_plan(registry, ["app"]).stages == [["core"], ["lib"], ["app"]]


def test_installed_is_case_insensitive():
    registry = Registry.from_mapping({
        "app": ("1.0", ["Lib"]),
        "lib": ("1.0", []),
    })
    plan = build_plan(registry, ["app"], installed=["LIB"])
    assert plan.stages == [["app"]]


def test_long_chain():
    n = 300
    mapping = {
        f"p{i}": ("1.0", [f"p{i + 1}"] if i + 1 < n else []) for i in range(n)
    }
    registry = Registry.from_mapping(mapping)
    order = Resolver(registry).resolve(["p0"])
    assert order == [f"p{i}" for i in range(n - 1, -1, -1)]
    plan = build_plan(registry, ["p0"])
    assert len(plan.stages) == n
    assert all(len(stage) == 1 for stage in plan.stages)


def test_random_dag_order_and_stages():
    n = 200
    deps, registry = _random_dag(n)
    roots = [f"p{n - 1}", f"p{n - 2}", f"p{n - 3}"]

    order = Resolver(registry).resolve(roots)
    position = {name: i for i, name in enumerate(order)}
    assert len(position) == len(order), "package listed twice"

    reachable = set()
    todo = [n - 1, n - 2, n - 3]
    while todo:
        i = todo.pop()
        if i in reachable:
            continue
        reachable.add(i)
        todo.extend(deps[i])
    assert set(position) == {f"p{i}" for i in reachable}
    for i in reachable:
        for j in deps[i]:
            assert position[f"p{j}"] < position[f"p{i}"]

    level = {}
    for i in range(n):
        level[i] = 1 + max(level[j] for j in deps[i]) if deps[i] else 0
    plan = build_plan(registry, roots)
    stage_of = {name: s for s, stage in enumerate(plan.stages) for name in stage}
    assert set(stage_of) == set(position)
    for i in reachable:
        assert stage_of[f"p{i}"] == level[i]
    flat = {name: k for k, name in enumerate(plan.order)}
    for i in reachable:
        for j in deps[i]:
            assert flat[f"p{j}"] < flat[f"p{i}"]
