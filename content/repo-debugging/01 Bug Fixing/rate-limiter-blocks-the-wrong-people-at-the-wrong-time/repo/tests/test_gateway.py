from ratelimit.gateway import Gateway
from ratelimit.limiter import RateLimiter
from ratelimit.policy import Policy


def make_gateway(limit, window=10):
    return Gateway(RateLimiter(Policy(limit, window)))


def test_ok_response_reports_remaining():
    gw = make_gateway(3)
    r = gw.handle("alice", "search", 0)
    assert r.status == 200
    assert r.headers["X-RateLimit-Remaining"] == "2"


def test_rejected_response_has_retry_after():
    gw = make_gateway(1)
    assert gw.handle("alice", "search", 0).status == 200
    r = gw.handle("alice", "search", 4.5)
    assert r.status == 429
    assert r.headers["Retry-After"] == "6"
