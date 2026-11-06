from pkgres import CycleError, MissingPackage, Registry, Resolver, VersionConflict


def _raises(exc_type, func, *args):
    try:
        func(*args)
    except exc_type as exc:
        return exc
    raise AssertionError(f"{exc_type.__name__} not raised")


def test_linear_chain():
    registry = Registry.from_mapping({
        "app": ("1.0", ["lib"]),
        "lib": ("1.0", ["core"]),
        "core": ("1.0", []),
    })
    assert Resolver(registry).resolve(["app"]) == ["core", "lib", "app"]


def test_diamond_is_not_a_cycle():
    registry = Registry.from_mapping({
        "app": ("1.0", ["left", "right"]),
        "left": ("1.0", ["base"]),
        "right": ("1.0", ["base"]),
        "base": ("1.0", []),
    })
    order = Resolver(registry).resolve(["app"])
    assert order == ["base", "left", "right", "app"]


def test_real_cycle_is_reported():
    registry = Registry.from_mapping({
        "a": ("1.0", ["b"]),
        "b": ("1.0", ["a"]),
    })
    exc = _raises(CycleError, Resolver(registry).resolve, ["a"])
    assert exc.chain == ["a", "b", "a"]


def test_missing_package():
    registry = Registry.from_mapping({"app": ("1.0", ["ghost"])})
    exc = _raises(MissingPackage, Resolver(registry).resolve, ["app"])
    assert exc.name == "ghost"


def test_version_conflict():
    registry = Registry.from_mapping({
        "app": ("1.0", ["lib>=2.0"]),
        "lib": ("1.5", []),
    })
    exc = _raises(VersionConflict, Resolver(registry).resolve, ["app"])
    assert exc.required_by == "app"


def test_two_digit_minor_version_is_accepted():
    registry = Registry.from_mapping({
        "app": ("1.0", ["lib>=1.9"]),
        "lib": ("1.10.0", []),
    })
    assert Resolver(registry).resolve(["app"]) == ["lib", "app"]
