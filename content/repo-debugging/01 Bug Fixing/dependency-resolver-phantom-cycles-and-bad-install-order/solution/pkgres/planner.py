"""Turns a resolved install order into parallel installation stages."""

from dataclasses import dataclass, field

from .resolver import Resolver


@dataclass
class Plan:
    """Install stages; packages within one stage can be installed in parallel."""

    stages: list = field(default_factory=list)

    @property
    def order(self):
        """All package names, stage by stage."""
        return [name for stage in self.stages for name in stage]

    def __len__(self):
        return sum(len(stage) for stage in self.stages)


def build_plan(registry, roots, installed=()):
    """Resolve ``roots`` and group the packages into stages.

    Packages listed in ``installed`` are left out of the plan. A package is
    placed in the stage after the latest stage of its dependencies; packages
    without pending dependencies go into stage 0.
    """
    skip = {name.lower() for name in installed}
    pending = [name for name in Resolver(registry).resolve(roots) if name not in skip]

    levels = {}
    for name in pending:
        dep_levels = [
            levels[dep.name]
            for dep in registry.get(name).requirements()
            if dep.name in levels
        ]
        levels[name] = 1 + max(dep_levels) if dep_levels else 0

    stages = []
    for name in pending:
        while len(stages) <= levels[name]:
            stages.append([])
        stages[levels[name]].append(name)
    for stage in stages:
        stage.sort()
    return Plan(stages)
