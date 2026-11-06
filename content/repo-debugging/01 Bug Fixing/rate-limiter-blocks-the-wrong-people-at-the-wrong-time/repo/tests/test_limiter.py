from ratelimit.limiter import RateLimiter
from ratelimit.policy import Policy


def make(limit=3, window=10):
    return RateLimiter(Policy(limit, window))


def test_allows_up_to_limit():
    rl = make(limit=3)
    results = [rl.check("alice", "search", t).allowed for t in (0, 1, 2)]
    assert results == [True, True, True]


def test_blocks_over_limit_with_retry_after():
    rl = make(limit=1, window=10)
    assert rl.check("alice", "search", 0).allowed
    d = rl.check("alice", "search", 4)
    assert not d.allowed
    assert d.retry_after == 6


def test_users_in_same_org_have_separate_buckets():
    rl = make(limit=2)
    assert rl.check("acme/alice", "search", 0).allowed
    assert rl.check("acme/alice", "search", 1).allowed
    assert not rl.check("acme/alice", "search", 2).allowed
    assert rl.check("acme/bob", "search", 2).allowed, "bob has not used any quota"


def test_endpoints_are_tracked_separately():
    rl = make(limit=1)
    assert rl.check("alice", "search", 0).allowed
    assert rl.check("alice", "upload", 1).allowed


def test_allowed_again_exactly_one_window_later():
    rl = make(limit=1, window=10)
    assert rl.check("alice", "search", 0).allowed
    assert not rl.check("alice", "search", 5).allowed
    assert rl.check("alice", "search", 10).allowed
