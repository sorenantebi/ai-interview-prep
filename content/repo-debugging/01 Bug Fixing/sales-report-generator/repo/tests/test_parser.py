from salesreport.parser import parse_sales


def test_parse_basic():
    sales = parse_sales("region,rep,amount\nEU,Alice,100.50\nUS,Bob,20\n")
    assert len(sales) == 2
    assert sales[0].region == "EU"
    assert sales[0].rep == "Alice"
    assert sales[0].amount == 100.5
    assert sales[1].amount == 20.0


def test_parse_strips_whitespace_and_money_symbols():
    text = 'Region, Rep ,Amount\n EU , Alice ,"$1,200.50"\n'
    sales = parse_sales(text)
    assert len(sales) == 1
    assert sales[0].region == "EU"
    assert sales[0].rep == "Alice"
    assert sales[0].amount == 1200.5


def test_parse_skips_blank_rows():
    sales = parse_sales("region,rep,amount\nEU,Alice,10\n,,\n\nUS,Bob,5\n")
    assert [s.rep for s in sales] == ["Alice", "Bob"]


def test_parse_missing_column_raises():
    try:
        parse_sales("region,amount\nEU,10\n")
    except ValueError:
        return
    assert False, "expected ValueError for missing 'rep' column"
