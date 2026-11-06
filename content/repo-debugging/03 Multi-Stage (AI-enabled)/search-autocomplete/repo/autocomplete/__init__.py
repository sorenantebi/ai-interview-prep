"""Search autocomplete: a phrase index and the service on top of it."""

from autocomplete.models import Suggestion
from autocomplete.service import AutocompleteService

__all__ = ["AutocompleteService", "Suggestion"]
