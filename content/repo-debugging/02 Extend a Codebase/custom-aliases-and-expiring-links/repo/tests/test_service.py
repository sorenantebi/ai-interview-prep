from shortener.clock import FakeClock
from shortener.errors import InvalidUrlError, LinkNotFoundError
from shortener.service import ShortenerService


def raises(exc_type, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc_type:
        return True
    return False


def make_service():
    clock = FakeClock()
    return ShortenerService(clock=clock), clock


def test_generated_codes_are_sequential():
    svc, _ = make_service()
    assert svc.shorten("https://example.com/a") == "1000"
    assert svc.shorten("https://example.com/b") == "1001"


def test_resolve_returns_url_and_counts_hits():
    svc, _ = make_service()
    code = svc.shorten("  https://example.com/page  ")
    assert svc.resolve(code) == "https://example.com/page"
    svc.resolve(code)
    assert svc.stats(code).hits == 2


def test_unknown_code_raises():
    svc, _ = make_service()
    assert raises(LinkNotFoundError, svc.resolve, "nope")
    assert raises(LinkNotFoundError, svc.stats, "nope")


def test_invalid_urls_are_rejected():
    svc, _ = make_service()
    for bad in ("", "example.com", "ftp://example.com/x", "https://", None):
        assert raises(InvalidUrlError, svc.shorten, bad), bad


def test_created_at_comes_from_injected_clock():
    svc, clock = make_service()
    start = clock.now()
    code = svc.shorten("https://example.com/")
    clock.advance(30)
    assert svc.stats(code).created_at == start
