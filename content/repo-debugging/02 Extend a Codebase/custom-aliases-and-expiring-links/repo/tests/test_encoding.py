from shortener.encoding import decode, encode


def test_encode_known_values():
    assert encode(0) == "0"
    assert encode(61) == "Z"
    assert encode(62) == "10"
    assert encode(62 ** 3) == "1000"


def test_decode_roundtrip():
    for n in (0, 1, 61, 62, 3843, 238328, 10 ** 12):
        assert decode(encode(n)) == n, n
