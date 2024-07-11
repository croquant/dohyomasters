import unittest

from .base26 import decode, encode


class TestBase26EncodeDecode(unittest.TestCase):
    def test_encode_decode(self) -> None:
        test_strings = [
            b"hello world",
            b"this is a test",
            b"abcdefghijklmnopqrstuvwxyz",
            b"1234567890",
            b"!@#$%^&*()_+",
            b"Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        ]

        for s in test_strings:
            encoded = encode(s)
            decoded = decode(encoded)
            assert decoded == s

    def test_long_string(self) -> None:
        long_input = b"abcdefghijklmnopqrstuvwxyz" * 100
        encoded = encode(long_input)
        decoded = decode(encoded)
        assert decoded == long_input

    def test_special_characters(self) -> None:
        special_input = b"!@#$%^&*()_+"
        encoded = encode(special_input)
        decoded = decode(encoded)
        assert decoded == special_input


if __name__ == "__main__":
    unittest.main()
