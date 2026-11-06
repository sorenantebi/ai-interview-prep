from autocomplete.loader import parse_lines
from autocomplete.models import Suggestion
from autocomplete.service import AutocompleteService


def test_record_accumulates_counts():
    service = AutocompleteService()
    assert service.record("pizza") is True
    service.record("pizza", 3)
    assert service.count("pizza") == 4
    assert len(service) == 1


def test_record_rejects_non_positive_counts():
    service = AutocompleteService()
    for bad in (0, -2):
        try:
            service.record("pizza", bad)
        except ValueError:
            pass
        else:
            assert False, "expected ValueError for count=%r" % bad
    assert len(service) == 0


def test_blank_phrases_are_ignored():
    service = AutocompleteService()
    assert service.record("   ") is False
    assert service.record(None) is False
    assert len(service) == 0


def test_load_from_log_lines():
    lines = ["pizza\t3\n", "\n", "pasta bake\t2\n", "pizza\t1\n"]
    service = AutocompleteService()
    assert service.load(parse_lines(lines)) == 3
    assert service.count("pizza") == 4
    assert len(service) == 2


def test_suggest_returns_ranked_suggestions():
    service = AutocompleteService()
    service.load([("pizza", 5), ("pizza hut", 9), ("pasta", 5)])
    assert service.suggest("pi") == [Suggestion("pizza hut", 9), Suggestion("pizza", 5)]
    assert service.suggest("p", k=2) == [Suggestion("pizza hut", 9), Suggestion("pasta", 5)]
    assert service.suggest("p", k=0) == []


def test_suggest_ignores_case_and_spacing():
    service = AutocompleteService()
    service.record("New York", 5)
    service.record("new\tyork times", 3)
    service.record("  NEW   YORKER ", 3)
    result = service.suggest("  New  Y")
    assert [s.phrase for s in result] == ["new york", "new york times", "new yorker"]
    assert [s.count for s in result] == [5, 3, 3]
