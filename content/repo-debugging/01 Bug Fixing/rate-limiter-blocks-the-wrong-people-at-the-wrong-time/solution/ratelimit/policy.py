"""Rate limit configuration."""


class Policy:
    """Request quota: ``limit`` requests per ``window`` seconds.

    ``overrides`` maps an endpoint name to a limit that replaces the default
    for that endpoint only. The window length is the same for all endpoints.
    """

    def __init__(self, limit, window, overrides=None):
        if limit <= 0:
            raise ValueError("limit must be positive")
        if window <= 0:
            raise ValueError("window must be positive")
        self.limit = limit
        self.window = window
        self.overrides = dict(overrides) if overrides else {}

    def limit_for(self, endpoint):
        """Return the number of requests allowed on ``endpoint`` per window."""
        return self.overrides.get(endpoint, self.limit)

    def set_override(self, endpoint, limit):
        """Give ``endpoint`` its own limit."""
        if limit <= 0:
            raise ValueError("limit must be positive")
        self.overrides[endpoint] = limit
