"""Small string helpers shared across the package."""


def normalize_path(path):
    """Collapse a request path into a stable endpoint pattern.

    The query string and any trailing slash are dropped and purely numeric
    segments are replaced with ``:id``, so ``/api/users/42/?x=1`` becomes
    ``/api/users/:id``.
    """
    path = path.split("?", 1)[0]
    if len(path) > 1:
        path = path.rstrip("/")
    parts = [":id" if part.isdigit() else part for part in path.split("/")]
    return "/".join(parts)
