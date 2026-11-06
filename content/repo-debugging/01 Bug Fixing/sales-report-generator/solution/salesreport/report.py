"""Build the text report shown in the weekly sales meeting."""

from salesreport.aggregate import region_totals, rep_totals
from salesreport.parser import parse_sales
from salesreport.utils import format_money


def top_seller(sales):
    """Return ``(rep, total)`` for the rep with the highest total.

    Ties are broken alphabetically by rep name. Returns None if there are no
    sales.
    """
    totals = rep_totals(sales)
    if not totals:
        return None
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return ranked[0]


def format_report(sales):
    """Render a list of sales as the report text (no trailing newline)."""
    if not sales:
        return "No sales."

    lines = ["Region totals:"]
    for region, total in sorted(region_totals(sales).items()):
        lines.append(f"  {region}: {format_money(total)}")

    rep, total = top_seller(sales)
    lines.append(f"Top seller: {rep} ({format_money(total)})")
    return "\n".join(lines)


def build_report(csv_text):
    """Parse CSV text and return the formatted report."""
    return format_report(parse_sales(csv_text))
