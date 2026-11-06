"""In-memory phrase index."""


class PhraseIndex:
    """Stores normalised phrases together with their search counts.

    Keys are expected to be normalised already (see ``autocomplete.text``).
    """

    def __init__(self):
        self._counts = {}

    def __len__(self):
        return len(self._counts)

    def __contains__(self, phrase):
        return phrase in self._counts

    def count(self, phrase):
        """Return the recorded count of ``phrase`` (0 if it is unknown)."""
        return self._counts.get(phrase, 0)

    def add(self, phrase, count=1):
        """Increase the count of ``phrase`` by ``count`` and return the new total."""
        total = self._counts.get(phrase, 0) + count
        self._counts[phrase] = total
        return total

    def top_k(self, prefix, k):
        """Return up to ``k`` ``(phrase, count)`` pairs for phrases starting with ``prefix``.

        Pairs are ordered by count, highest first; phrases with equal counts
        are ordered alphabetically. The empty prefix matches every phrase.
        """
        raise NotImplementedError("top_k is not implemented yet")
