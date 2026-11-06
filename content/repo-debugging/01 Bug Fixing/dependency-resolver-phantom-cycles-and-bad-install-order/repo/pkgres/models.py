"""Data classes describing packages and their requirements."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Requirement:
    """A dependency on a package name with an optional version spec."""

    name: str
    spec: str = ""


def parse_requirement(text):
    """Parse ``"libb>=1.2,<2"`` into ``Requirement("libb", ">=1.2,<2")``."""
    text = text.strip()
    end = 0
    while end < len(text) and (text[end].isalnum() or text[end] in "-_"):
        end += 1
    name = text[:end]
    if not name:
        raise ValueError(f"invalid requirement: {text!r}")
    return Requirement(name.lower(), text[end:].strip())


@dataclass
class Package:
    """A published package: a name, a version and its requirement strings."""

    name: str
    version: str
    requires: list = field(default_factory=list)

    def requirements(self):
        """Return the parsed requirements in declaration order."""
        return [parse_requirement(text) for text in self.requires]
