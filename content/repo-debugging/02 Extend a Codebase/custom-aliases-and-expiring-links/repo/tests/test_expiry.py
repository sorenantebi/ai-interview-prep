from shortener.clock import FakeClock
from shortener.errors import LinkExpiredError, LinkNotFoundError
from shortener.service import ShortenerService

URL = "https://example.com/campaign"


def raises(exc_type, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc_type:
        return True
    return False


def make_service():
    clock = FakeClock()
    return ShortenerService(clock=clock), clock


def test_link_without_ttl_never_expires():
    svc, clock = make_service()
    code = svc.shorten(URL)
    clock.advance(10 * 365 * 24 * 3600)
    assert svc.resolve(code) == URL
    assert svc.stats(code).expires_at is None


def test_link_expires_exactly_at_ttl():
    svc, clock = make_service()
    code = svc.shorten(URL, ttl=60)
    clock.advance(59)
    assert svc.resolve(code) == URL
    clock.advance(1)
    assert raises(LinkExpiredError, svc.resolve, code)
    assert raises(LinkExpiredError, svc.stats, code)


def test_stats_exposes_expires_at():
    svc, clock = make_service()
    svc.shorten(URL, alias="sale", ttl=120)
    assert svc.stats("sale").expires_at == clock.now() + 120


def test_purge_removes_only_expired_links():
    svc, clock = make_service()
    svc.shorten(URL, alias="short1", ttl=10)
    generated = svc.shorten(URL, ttl=10)
    keep = svc.shorten(URL)
    clock.advance(10)
    assert svc.purge_expired() == 2
    assert svc.resolve(keep) == URL
    assert raises(LinkNotFoundError, svc.resolve, "short1")
    assert raises(LinkNotFoundError, svc.resolve, generated)
