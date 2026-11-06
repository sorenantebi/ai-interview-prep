from kvstore.cli import Interpreter


def test_basic_commands():
    cli = Interpreter()
    assert cli.execute("SET a hello world") == "OK"
    assert cli.execute("GET a") == "hello world"
    assert cli.execute("get missing") == "NULL"
    assert cli.execute("DELETE a") == "1"
    assert cli.execute("DELETE a") == "0"
    assert cli.execute("") is None


def test_errors_are_replies():
    cli = Interpreter()
    assert cli.execute("FLY away") == "ERROR: unknown command: FLY"
    assert cli.execute("GET") == "ERROR: usage: GET key"


def test_nested_transaction_script():
    cli = Interpreter()
    script = "\n".join(
        [
            "SET a 10",
            "BEGIN",
            "SET a 20",
            "BEGIN",
            "SET a 30",
            "GET a",
            "ROLLBACK",
            "GET a",
            "ROLLBACK",
            "GET a",
            "ROLLBACK",
        ]
    )
    assert cli.run(script) == [
        "OK", "OK", "OK", "OK", "OK", "30", "OK", "20", "OK", "10",
        "ERROR: no active transaction",
    ]
