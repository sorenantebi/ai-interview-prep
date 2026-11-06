"""Helpers for turning a user and an endpoint into a storage key."""


def split_user_id(user_id):
    """Split ``"org/name"`` into ``(org, name)``.

    Ids without a slash have no organisation and yield ``("", user_id)``.
    """
    org, sep, name = user_id.partition("/")
    if not sep:
        return "", user_id
    return org, name


def bucket_key(user_id, endpoint):
    """Return the key under which a user's hits on an endpoint are stored."""
    org, name = split_user_id(user_id)
    return f"{endpoint}|{org}|{name}"
