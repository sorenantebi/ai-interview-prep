"""Data model for catalog records."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    """A single product in the catalog."""

    id: int
    name: str
    category: str
    price_cents: int

    def to_dict(self):
        """Return a JSON-serialisable representation of the record."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price_cents": self.price_cents,
        }
