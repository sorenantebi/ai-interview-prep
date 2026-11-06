from shortener.clock import FakeClock
from shortener.errors import (
    AliasTakenError,
    InvalidAliasError,
    InvalidUrlError,
    LinkExpiredError,
    LinkNotFoundError,
)
from shortener.service import ShortenerService
from shortener.storage import LinkStore

URL = "https://example.com/x"
OTHER = "https://example.com/y"


def raises(exc_type, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc_type:
        return True
    return False


def make(store=None):
    clock = FakeClock()
    return ShortenerService(store=store, clock=clock), clock


def test_alias_length_boundaries():
    svc, _ = make()
    assert svc.shorten(URL, alias="abc") == "abc"
    assert svc.shorten(URL, alias="a" * 32) == "a" * 32
    assert raises(InvalidAliasError, svc.shorten, URL, alias="ab")
    assert raises(InvalidAliasError, svc.shorten, URL, alias="a" * 33)


def test_alias_allows_dash_and_underscore():
    svc, _ = make()
    assert svc.shorten(URL, alias="a-b_c") == "a-b_c"


def test_alias_trailing_newline_is_invalid():
    svc, _ = make()
    assert raises(InvalidAliasError, svc.shorten, URL, alias="abc\n")
    assert raises(InvalidAliasError, svc.shorten, URL, alias=" abc")


def test_alias_must_be_ascii():
    svc, _ = make()
    for bad in ("café", "naïve1", "日本語リンク"):
        assert raises(InvalidAliasError, svc.shorten, URL, alias=bad), bad


def test_alias_must_be_a_string():
    svc, _ = make()
    assert raises(InvalidAliasError, svc.shorten, URL, alias=12345)


def test_aliases_are_case_sensitive():
    svc, _ = make()
    svc.shorten(URL, alias="Docs")
    svc.shorten(OTHER, alias="docs")
    assert svc.resolve("Docs") == URL
    assert svc.resolve("docs") == OTHER


def test_reserved_aliases_rejected_in_any_case():
    svc, _ = make()
    for bad in ("api", "API", "Health", "STATIC", "aDmIn"):
        assert raises(InvalidAliasError, svc.shorten, URL, alias=bad), bad
    # names that merely contain a reserved word are fine
    assert svc.shorten(URL, alias="api-docs") == "api-docs"


def test_url_is_validated_before_alias():
    svc, _ = make()
    assert raises(InvalidUrlError, svc.shorten, "nope", alias="x")


def test_rejected_calls_store_nothing():
    store = LinkStore()
    svc, _ = make(store)
    assert raises(InvalidAliasError, svc.shorten, URL, alias="no")
    assert raises(ValueError, svc.shorten, URL, ttl=0)
    assert raises(ValueError, svc.shorten, URL, alias="fine", ttl=-1)
    assert raises(InvalidUrlError, svc.shorten, "bad", ttl=5)
    assert len(store) == 0


def test_alias_does_not_consume_a_sequence_number():
    svc, _ = make()
    svc.shorten(URL, alias="mine")
    assert svc.shorten(OTHER) == "1000"


def test_generated_codes_skip_every_taken_alias():
    svc, _ = make()
    svc.shorten(URL, alias="1000")
    svc.shorten(URL, alias="1001")
    assert svc.shorten(OTHER) == "1002"


def test_alias_registered_ahead_of_the_counter_is_skipped_later():
    svc, _ = make()
    svc.shorten(URL, alias="1005")
    codes = [svc.shorten(OTHER) for _ in range(8)]
    assert len(set(codes)) == 8
    assert "1005" not in codes
    assert svc.resolve("1005") == URL


def test_non_positive_ttl_raises_value_error():
    svc, _ = make()
    assert raises(ValueError, svc.shorten, URL, ttl=0)
    assert raises(ValueError, svc.shorten, URL, ttl=-1)
    assert raises(ValueError, svc.shorten, URL, ttl=-0.5)


def test_fractional_ttl_and_expires_at():
    svc, clock = make()
    code = svc.shorten(URL, ttl=0.5)
    record = svc.stats(code)
    assert record.expires_at == record.created_at + 0.5
    clock.advance(0.25)
    assert svc.resolve(code) == URL
    clock.advance(0.25)
    assert raises(LinkExpiredError, svc.resolve, code)


def test_expired_link_does_not_count_hits():
    store = LinkStore()
    svc, clock = make(store)
    code = svc.shorten(URL, ttl=5)
    svc.resolve(code)
    clock.advance(5)
    assert raises(LinkExpiredError, svc.resolve, code)
    assert raises(LinkExpiredError, svc.resolve, code)
    assert store.get(code).hits == 1


def test_alias_stays_taken_until_expiry_then_can_be_reused():
    svc, clock = make()
    svc.shorten(URL, alias="promo", ttl=10)
    clock.advance(9)
    assert raises(AliasTakenError, svc.shorten, OTHER, alias="promo")
    assert svc.resolve("promo") == URL
    clock.advance(1)
    assert svc.shorten(OTHER, alias="promo") == "promo"
    assert svc.resolve("promo") == OTHER


def test_reused_alias_starts_fresh():
    svc, clock = make()
    svc.shorten(URL, alias="promo", ttl=10)
    clock.advance(5)
    svc.resolve("promo")
    clock.advance(5)
    svc.shorten(OTHER, alias="promo")
    record = svc.stats("promo")
    assert record.hits == 0
    assert record.expires_at is None
    assert record.created_at == clock.now()
    clock.advance(10 ** 6)
    assert svc.resolve("promo") == OTHER


def test_purge_counts_and_is_idempotent():
    store = LinkStore()
    svc, clock = make(store)
    svc.shorten(URL, ttl=1)
    svc.shorten(URL, ttl=100)
    svc.shorten(URL)
    clock.advance(1)
    assert svc.purge_expired() == 1
    assert len(store) == 2
    assert svc.purge_expired() == 0
    clock.advance(100)
    assert svc.purge_expired() == 1
    assert len(store) == 1


def test_purged_code_becomes_not_found_and_alias_reusable():
    svc, clock = make()
    svc.shorten(URL, alias="gone", ttl=3)
    clock.advance(3)
    assert raises(LinkExpiredError, svc.stats, "gone")
    svc.purge_expired()
    assert raises(LinkNotFoundError, svc.stats, "gone")
    assert svc.shorten(OTHER, alias="gone") == "gone"
