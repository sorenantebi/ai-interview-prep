"""Exceptions raised while resolving dependencies."""


class ResolverError(Exception):
    """Base class for all resolver failures."""


class MissingPackage(ResolverError):
    """A required package is not present in the registry."""

    def __init__(self, name, required_by=None):
        self.name = name
        self.required_by = required_by
        origin = f" (required by {required_by})" if required_by else ""
        super().__init__(f"package not found: {name}{origin}")


class VersionConflict(ResolverError):
    """The available version of a package does not satisfy a requirement."""

    def __init__(self, requirement, found, required_by=None):
        self.requirement = requirement
        self.found = found
        self.required_by = required_by
        origin = f" (required by {required_by})" if required_by else ""
        super().__init__(
            f"{requirement.name}{requirement.spec} is not satisfied "
            f"by available version {found}{origin}"
        )


class CycleError(ResolverError):
    """The dependency graph contains a cycle.

    ``chain`` lists the packages forming the cycle; the first and the last
    entry are the same package.
    """

    def __init__(self, chain):
        self.chain = list(chain)
        super().__init__("dependency cycle: " + " -> ".join(self.chain))
