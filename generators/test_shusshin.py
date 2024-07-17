import unittest
from unittest.mock import patch

from .shusshin import ShusshinGenerator, get_pref_probs


class TestShusshinGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ShusshinGenerator()

    def test_get_japanese(self):
        # Mock the random.choices function to always return "Tokyo"
        with patch("random.choices", return_value=["Tokyo"]):
            shusshin = self.generator.get_japanese()
            self.assertEqual(shusshin.prefecture, "Tokyo")

    def test_get(self):
        # Mock the random.choices function to always return "Osaka"
        with patch("random.choices", return_value=["Osaka"]):
            shusshin = self.generator.get()
            self.assertEqual(shusshin.prefecture, "Osaka")

    def test_get_pref_probs(self):
        # Ensure that the probabilities sum up to 1
        pref_probs = get_pref_probs()
        total_prob = sum(pref_probs.values())
        self.assertAlmostEqual(total_prob, 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
