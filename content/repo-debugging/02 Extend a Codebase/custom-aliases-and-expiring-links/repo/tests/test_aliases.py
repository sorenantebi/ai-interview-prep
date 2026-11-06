from shortener.clock import FakeClock
from shortener.errors import AliasTakenError, InvalidAliasError
from shortener.service import ShortenerService


def raises(exc_type, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc_type:
        return True
    return False


def make_service():
    return ShortenerService(clock=FakeClock())


def test_custom_alias_is_used_as_code():
    svc = make_service()
    code = svc.shorten("https://example.com/sale", alias="spring-sale")
    assert code == "spring-sale"
    assert svc.resolve("spring-sale") == "https://example.com/sale"


def test_invalid_aliases_are_rejected():
    svc = make_service()
    for bad in ("ab", "a" * 33, "has space", "semi;colon", "api", "Admin"):
        assert raises(InvalidAliasError, svc.shorten, "https://example.com/", alias=bad), bad


def test_taken_alias_is_rejected_and_original_kept():
    svc = make_service()
    svc.shorten("https://example.com/one", alias="docs")
    assert raises(AliasTakenError, svc.shorten, "https://example.com/two", alias="docs")
    assert svc.resolve("docs") == "https://example.com/one"


def test_generated_code_never_overwrites_an_alias():
    svc = make_service()
    svc.shorten("https://example.com/alias", alias="1000")
    code = svc.shorten("https://example.com/generated")
    assert code != "1000"
    assert svc.resolve("1000") == "https://example.com/alias"
    assert svc.resolve(code) == "https://example.com/generated"
