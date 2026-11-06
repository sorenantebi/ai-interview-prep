"""Depth-first dependency resolution."""

from .errors import CycleError, MissingPackage, VersionConflict
from .models import parse_requirement
from .versions import satisfies


class _State:
    """Bookkeeping for one call to :meth:`Resolver.resolve`."""

    def __init__(self):
        self.visited = set()
        self.stack = []
        self.order = []


class Resolver:
    """Computes an install order for a set of requested packages."""

    def __init__(self, registry):
        self.registry = registry

    def resolve(self, roots):
        """Return package names, dependencies first, each name exactly once.

        ``roots`` is a list of requirement strings. Raises ``MissingPackage``,
        ``VersionConflict`` or ``CycleError`` when the request cannot be met.
        """
        state = _State()
        for text in roots:
            self._visit(parse_requirement(text), None, state)
        return state.order

    def _visit(self, requirement, parent, state):
        name = requirement.name
        if name not in self.registry:
            raise MissingPackage(name, parent)
        package = self.registry.get(name)
        if not satisfies(package.version, requirement.spec):
            raise VersionConflict(requirement, package.version, parent)

        if name in state.visited:
            raise CycleError(state.stack + [name])
        state.visited.add(name)
        state.stack.append(name)
        for dependency in package.requirements():
            self._visit(dependency, name, state)
        state.stack.pop()
        state.order.append(name)
