"""Request handlers: glue between query parameters, storage and pagination."""

from catalog.pagination import paginate, total_pages
from catalog.params import ParamError, parse_pagination


def list_records(repo, query):
    """Handle a listing request.

    ``query`` supports ``page``, ``page_size``, ``category`` and ``sort``.
    Returns a ``(status_code, body)`` tuple.
    """
    try:
        page, page_size = parse_pagination(query)
    except ParamError as exc:
        return 400, {"error": str(exc)}

    try:
        records = repo.query(
            category=query.get("category"),
            sort_by=query.get("sort", "id"),
        )
    except ValueError as exc:
        return 400, {"error": str(exc)}

    result = paginate(records, page, page_size)
    return 200, {
        "items": [r.to_dict() for r in result.items],
        "page": result.page,
        "page_size": result.page_size,
        "total": result.total,
        "total_pages": total_pages(result.total, result.page_size),
        "has_next": result.has_next,
    }
