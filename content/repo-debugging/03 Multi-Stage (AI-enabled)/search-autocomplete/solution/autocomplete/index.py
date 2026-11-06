"""In-memory phrase index backed by a trie with cached top-k lists."""

import bisect
import heapq

CACHE_SIZE = 10


class _Node:
    """A trie node. ``top`` holds the best entries of the whole subtree.

    Entries are ``(-count, phrase)`` tuples kept sorted, so the natural tuple
    order is "highest count first, then alphabetical".
    """

    __slots__ = ("children", "top")

    def __init__(self):
        self.children = {}
        self.top = []


class PhraseIndex:
    """Stores normalised phrases together with their search counts.

    Keys are expected to be normalised already (see ``autocomplete.text``).
    """

    def __init__(self):
        self._counts = {}
        self._root = _Node()

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
        entry = (-total, phrase)
        node = self._root
        self._refresh(node.top, entry)
        for ch in phrase:
            child = node.children.get(ch)
            if child is None:
                child = node.children[ch] = _Node()
            node = child
            self._refresh(node.top, entry)
        return total

    @staticmethod
    def _refresh(top, entry):
        """Insert the new ``entry`` of a phrase into a node's sorted top list.

        Counts only grow, so a phrase that is not in a full list and ranks
        below its last entry can never belong there.
        """
        if len(top) >= CACHE_SIZE and entry > top[-1]:
            return
        phrase = entry[1]
        for i, (_, other) in enumerate(top):
            if other == phrase:
                del top[i]
                break
        bisect.insort(top, entry)
        del top[CACHE_SIZE:]

    def top_k(self, prefix, k):
        """Return up to ``k`` ``(phrase, count)`` pairs for phrases starting with ``prefix``.

        Pairs are ordered by count, highest first; phrases with equal counts
        are ordered alphabetically. The empty prefix matches every phrase.
        """
        if k < 1:
            return []
        node = self._root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return []
        if k <= CACHE_SIZE or len(node.top) < CACHE_SIZE:
            return [(phrase, -neg) for neg, phrase in node.top[:k]]
        found = []
        self._collect(node, prefix, found)
        return [(phrase, -neg) for neg, phrase in heapq.nsmallest(k, found)]

    def _collect(self, node, path, out):
        """Append ``(-count, phrase)`` for every phrase in the subtree of ``node``."""
        stack = [(node, path)]
        while stack:
            node, path = stack.pop()
            total = self._counts.get(path)
            if total is not None:
                out.append((-total, path))
            for ch, child in node.children.items():
                stack.append((child, path + ch))
