from ratelimit.gateway import Gateway
from ratelimit.limiter import RateLimiter
from ratelimit.policy import Policy
from ratelimit.window import SlidingWindow


def make(limit=2, window=10):
    return RateLimiter(Policy(limit, window))


def test_same_org_users_independent():
    rl = make(limit=1)
    assert rl.check("acme/alice", "api", 0).allowed
    assert not rl.check("acme/alice", "api", 1).allowed
    assert rl.check("acme/bob", "api", 1).allowed
    assert rl.check("acme/carol", "api", 1).allowed


def test_users_without_org_are_independent():
    rl = make(limit=1)
    assert rl.check("solo", "api", 0).allowed
    assert rl.check("other", "api", 0).allowed
    assert not rl.check("solo", "api", 1).allowed


def test_same_name_in_different_orgs_independent():
    rl = make(limit=1)
    assert rl.check("acme/alice", "api", 0).allowed
    assert rl.check("globex/alice", "api", 0).allowed
    assert not rl.check("acme/alice", "api", 1).allowed
    assert not rl.check("globex/alice", "api", 1).allowed


def test_org_prefix_and_bare_name_are_different_users():
    rl = make(limit=1)
    assert rl.check("alice", "api", 0).allowed
    assert rl.check("acme/alice", "api", 0).allowed


def test_boundary_chain_one_request_per_window():
    rl = make(limit=1, window=10)
    for t in (0, 10, 20, 30, 40):
        assert rl.check("alice", "api", t).allowed, f"request at t={t} should pass"


def test_boundary_with_partial_expiry():
    w = SlidingWindow(10)
    for t in (0, 3, 10):
        w.record(t)
    assert w.count(10) == 2
    assert w.count(13) == 1


def test_hit_just_inside_window_still_counts():
    w = SlidingWindow(10)
    w.record(0)
    assert w.count(9.999) == 1
    assert w.count(10) == 0


def test_float_boundary():
    rl = make(limit=1, window=2.5)
    assert rl.check("alice", "api", 0.5).allowed
    assert not rl.check("alice", "api", 2.9).allowed
    assert rl.check("alice", "api", 3.0).allowed


def test_denied_requests_not_recorded():
    rl = make(limit=2, window=10)
    assert rl.check("alice", "api", 0).allowed
    assert rl.check("alice", "api", 1).allowed
    for t in (2, 3, 4):
        assert not rl.check("alice", "api", t).allowed
    assert rl.check("alice", "api", 10).allowed
    assert rl.check("alice", "api", 11).allowed
    assert not rl.check("alice", "api", 11.5).allowed


def test_retry_after_value_when_denied():
    rl = make(limit=2, window=10)
    rl.check("alice", "api", 0)
    rl.check("alice", "api", 4)
    d = rl.check("alice", "api", 6)
    assert not d.allowed
    assert d.retry_after == 4
    assert d.remaining == 0


def test_allowed_decision_fields():
    rl = make(limit=3)
    d = rl.check("alice", "api", 0)
    assert d.allowed and d.remaining == 2 and d.retry_after == 0.0


def test_override_applies_in_limiter():
    policy = Policy(5, 10)
    policy.set_override("export", 1)
    rl = RateLimiter(policy)
    assert rl.check("alice", "export", 0).allowed
    assert not rl.check("alice", "export", 1).allowed
    for t in range(5):
        assert rl.check("alice", "search", t).allowed


def test_policy_instances_do_not_share_overrides():
    p1 = Policy(5, 10)
    p2 = Policy(5, 10)
    p1.set_override("a", 1)
    assert p2.overrides == {}
    p3 = Policy(3, 10)
    assert p3.limit_for("a") == 3


def test_passed_in_overrides_used_but_defaults_stay_clean():
    p = Policy(5, 10, {"a": 2})
    assert p.limit_for("a") == 2
    assert Policy(5, 10).limit_for("a") == 5


def test_reset_only_affects_target():
    rl = make(limit=1)
    rl.check("acme/alice", "api", 0)
    rl.check("acme/bob", "api", 0)
    rl.reset("acme/alice", "api")
    assert rl.check("acme/alice", "api", 1).allowed
    assert not rl.check("acme/bob", "api", 1).allowed


def test_gateway_retry_after_rounds_up():
    gw = Gateway(make(limit=1, window=10))
    assert gw.handle("alice", "api", 0).status == 200
    r = gw.handle("alice", "api", 9.2)
    assert r.status == 429
    assert r.headers["Retry-After"] == "1"


def test_gateway_remaining_counts_down():
    gw = Gateway(make(limit=3))
    remaining = [gw.handle("alice", "api", t).headers["X-RateLimit-Remaining"] for t in (0, 1, 2)]
    assert remaining == ["2", "1", "0"]


def test_gateway_edge_then_ok():
    gw = Gateway(make(limit=1, window=10))
    assert gw.handle("alice", "api", 0).status == 200
    assert gw.handle("alice", "api", 9.9).status == 429
    assert gw.handle("alice", "api", 10).status == 200


def test_many_users_isolated():
    rl = make(limit=2)
    for i in range(500):
        user = f"org{i % 7}/user{i}"
        assert rl.check(user, "api", 0).allowed
        assert rl.check(user, "api", 1).allowed
        assert not rl.check(user, "api", 2).allowed
