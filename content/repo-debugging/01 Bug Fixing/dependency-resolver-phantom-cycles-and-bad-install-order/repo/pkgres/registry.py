"""In-memory package index."""

from .errors import MissingPackage
from .models import Package


class Registry:
    """Maps case-insensitive package names to their available release."""

    def __init__(self, packages=()):
        self._packages = {}
        for package in packages:
            self.add(package)

    @classmethod
    def from_mapping(cls, mapping):
        """Build a registry from ``{name: (version, [requirement, ...])}``."""
        return cls(
            Package(name, version, list(requires))
            for name, (version, requires) in mapping.items()
        )

    def add(self, package):
        self._packages[package.name.lower()] = package

    def get(self, name):
        try:
            return self._packages[name.lower()]
        except KeyError:
            raise MissingPackage(name) from None

    def __contains__(self, name):
        return name.lower() in self._packages

    def __len__(self):
        return len(self._packages)
