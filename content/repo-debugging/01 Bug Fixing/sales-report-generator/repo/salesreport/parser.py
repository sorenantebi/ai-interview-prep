"""Parsing of the CSV sales export."""

import csv
import io

from salesreport.models import Sale
from salesreport.utils import parse_amount

REQUIRED_COLUMNS = ("region", "rep", "amount")


def parse_sales(csv_text):
    """Parse CSV text into a list of :class:`Sale` objects.

    Header names are matched case-insensitively and surrounding whitespace is
    ignored. Rows where all required fields are empty are skipped. Raises
    ValueError if a required column is missing or an amount is invalid.
    """
    reader = csv.DictReader(io.StringIO(csv_text))
    if reader.fieldnames is None:
        return []

    headers = [name.strip().lower() for name in reader.fieldnames]
    missing = [col for col in REQUIRED_COLUMNS if col not in headers]
    if missing:
        raise ValueError("missing column(s): " + ", ".join(missing))
    reader.fieldnames = headers

    sales = []
    for row in reader:
        region = (row.get("region") or "").strip()
        rep = (row.get("rep") or "").strip()
        amount_text = row.get("amount") or ""
        if not (region or rep or amount_text.strip()):
            continue
        sales.append(Sale(region=region, rep=rep, amount=parse_amount(amount_text)))
    return sales
