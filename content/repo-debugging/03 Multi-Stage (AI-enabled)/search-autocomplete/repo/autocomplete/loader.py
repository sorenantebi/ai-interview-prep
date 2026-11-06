"""Parsing of search-log lines into ``(phrase, count)`` pairs."""


def parse_line(line):
    """Parse one ``"<phrase>\\t<count>"`` log line.

    Returns ``None`` for blank lines and raises ``ValueError`` when the line
    has no tab-separated count.
    """
    text = line.rstrip("\r\n")
    if not text.strip():
        return None
    phrase, sep, raw = text.rpartition("\t")
    if not sep:
        raise ValueError("expected '<phrase><TAB><count>', got %r" % line)
    return phrase, int(raw)


def parse_lines(lines):
    """Yield ``(phrase, count)`` for every non-blank line."""
    for line in lines:
        parsed = parse_line(line)
        if parsed is not None:
            yield parsed
