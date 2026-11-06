"""Public entry point of the autocomplete package."""

from autocomplete.index import PhraseIndex
from autocomplete.models import Suggestion
from autocomplete.text import normalize

DEFAULT_K = 5


class AutocompleteService:
    """Records searched phrases and suggests completions for a prefix."""

    def __init__(self, index=None):
        self._index = index if index is not None else PhraseIndex()

    def __len__(self):
        return len(self._index)

    def record(self, phrase, count=1):
        """Register ``count`` searches for ``phrase``.

        Returns ``False`` when the phrase is empty after normalisation and
        nothing was recorded. Raises ``ValueError`` for a non-positive count.
        """
        if count < 1:
            raise ValueError("count must be positive")
        key = normalize(phrase)
        if not key:
            return False
        self._index.add(key, count)
        return True

    def load(self, pairs):
        """Record many ``(phrase, count)`` pairs; return how many were accepted."""
        accepted = 0
        for phrase, count in pairs:
            if self.record(phrase, count):
                accepted += 1
        return accepted

    def count(self, phrase):
        """Return the total number of recorded searches for ``phrase``."""
        return self._index.count(normalize(phrase))

    def suggest(self, prefix, k=DEFAULT_K):
        """Return up to ``k`` suggestions for ``prefix``, best first."""
        if k < 1:
            return []
        key = normalize(prefix)
        return [Suggestion(phrase, count) for phrase, count in self._index.top_k(key, k)]
