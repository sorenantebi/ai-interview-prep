---
difficulty: Hard
kind: bug-fix
---
# Dependency resolver: phantom cycles and bad install order

**Kind:** Bug fix · **Difficulty:** Hard

## Scenario
`pkgres` is the small package-dependency resolver behind our internal installer. Given a registry of packages and a list of requested packages, it computes an install order and groups the packages into stages that can be installed in parallel. Since the last release, several teams report that builds fail or misbehave. There is more than one defect, and fixing one may uncover another.

## Your tasks
1. Users report that some applications cannot be installed at all: the resolver reports a "dependency cycle" for package sets that have no cycle. The affected sets seem to have something in common, but nobody has pinned down what. Find and fix the cause (the failing tests show the symptoms).
2. Once the install plan could be generated, users found that a package is sometimes scheduled together with, or ahead of, one of its own dependencies, so the install fails on the first run. Find and fix the cause.
3. Packages whose version has a two-digit component (for example `1.10.0`) are rejected by constraints such as `>=1.9`, although they should be accepted. Find and fix the cause.

## Notes
- Entry points: `pkgres.build_plan(registry, roots, installed=())` and `Resolver(registry).resolve(roots)`. `roots` is a list of requirement strings such as `"app"` or `"lib>=1.2,<2"`.
- `resolve` returns package names so that every package appears after all of its dependencies and each package appears exactly once.
- `CycleError.chain` lists only the packages that form the cycle, and its first and last entries are the same package (for example `["a", "b", "a"]`).
- `Plan.stages` is a list of stages; packages in one stage can be installed in parallel, so a package must be in a strictly later stage than each of its dependencies. Names inside a stage are sorted.
- Package names are case-insensitive. Only the standard library is used.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
