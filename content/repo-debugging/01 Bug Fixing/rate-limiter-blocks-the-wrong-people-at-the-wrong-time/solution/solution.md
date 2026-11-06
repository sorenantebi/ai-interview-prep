# Rate limiter blocks the wrong people at the wrong time - Solution

## Root causes / approach

**1. Window edge counted too long: `ratelimit/window.py`, `SlidingWindow.prune`.**
The docstring says the window is the half-open interval `(now - size, now]`, so a hit made exactly `size` seconds ago is expired. `prune` used `self._hits[0] < cutoff`, which keeps a hit that sits exactly on the cutoff. At `t = 10` the request from `t = 0` therefore still counted, and the user was denied one tick too long. The fix is `<=`. The limiter then also returns a correct `retry_after`, because a denied request always has `oldest() > cutoff`, so the value is strictly positive.

**2. Users share a bucket: `ratelimit/keys.py`, `bucket_key`.**
`split_user_id` returns `(org, name)`, but `bucket_key` unpacked it as `org, _` and built the key from the organisation only. Every member of an organisation shared one window per endpoint, and every id without an organisation shared the single `""` bucket. The fix is to include both parts: `f"{endpoint}|{org}|{name}"`. Using only `name` would be wrong too, since `acme/alice` and `globex/alice` are different users. The hidden tests check this.

**3. Overrides leak between policies: `ratelimit/policy.py`, `Policy.__init__`.**
The default argument `overrides={}` is created once at function definition time. Every `Policy` built without explicit overrides received the same dict object, so `set_override("export", 1)` on one policy changed all of them. The fix is `overrides=None` and `self.overrides = dict(overrides) if overrides else {}`. Copying also stops later changes from touching a caller's dict.

## How to find it
- Start with `test_hit_expires_exactly_at_edge` in `tests/test_window.py`. It is the smallest failing test and points straight at `prune`. Compare the docstring's interval with the comparison operator.
- `test_users_in_same_org_have_separate_buckets` fails while a single-user test passes, so the problem is in how buckets are identified. Print `bucket_key("acme/alice", "search")` and `bucket_key("acme/bob", "search")`. Both return `search|acme`.
- `test_overrides_are_not_shared_between_policies` only passes if each `Policy` has its own dict. Check `first.overrides is second.overrides`, which prints `True`. A mutable default argument is the classic cause, and the signature confirms it.
- After the fixes, run the hidden-style cases yourself: an id without a slash, the same name in two organisations, and a chain of requests at 0, 10, 20.
