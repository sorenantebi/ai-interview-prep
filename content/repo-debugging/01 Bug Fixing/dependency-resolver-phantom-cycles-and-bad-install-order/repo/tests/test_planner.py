from pkgres import Registry, build_plan


def test_simple_chain_stages():
    registry = Registry.from_mapping({
        "app": ("1.0", ["lib"]),
        "lib": ("1.0", ["core"]),
        "core": ("1.0", []),
    })
    assert build_plan(registry, ["app"]).stages == [["core"], ["lib"], ["app"]]


def test_installed_packages_are_skipped():
    registry = Registry.from_mapping({
        "app": ("1.0", ["lib"]),
        "lib": ("1.0", ["core"]),
        "core": ("1.0", []),
    })
    plan = build_plan(registry, ["app"], installed=["core"])
    assert plan.stages == [["lib"], ["app"]]


def test_package_follows_its_deepest_dependency():
    registry = Registry.from_mapping({
        "app": ("1.0", ["lib", "tool"]),
        "lib": ("1.0", ["core"]),
        "tool": ("1.0", []),
        "core": ("1.0", []),
    })
    plan = build_plan(registry, ["app"])
    assert plan.stages == [["core", "tool"], ["lib"], ["app"]]


def test_diamond_plan():
    registry = Registry.from_mapping({
        "app": ("1.0", ["left", "right"]),
        "left": ("1.0", ["base"]),
        "right": ("1.0", ["base"]),
        "base": ("1.0", []),
    })
    plan = build_plan(registry, ["app"])
    assert plan.stages == [["base"], ["left", "right"], ["app"]]
    assert len(plan) == 4
