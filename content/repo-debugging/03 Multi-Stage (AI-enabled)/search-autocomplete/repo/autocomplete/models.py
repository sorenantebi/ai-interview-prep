"""Value types returned by the autocomplete service."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Suggestion:
    """A completion candidate together with its total search count."""

    phrase: str
    count: int

    def __str__(self):
        return self.phrase
