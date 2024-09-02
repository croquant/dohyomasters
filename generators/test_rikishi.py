import unittest
from unittest.mock import patch

from base.models import GameDate
from generators.rikishi import (
    AVG_POTENTIAL,
    MAX_POTENTIAL,
    MIN_POTENTIAL,
    RikishiGenerator,
)
from rikishi.models import Rikishi, RikishiStats, Shusshin


class TestRikishiGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = RikishiGenerator()

    @patch("generators.rikishi.RikishiNameGenerator.get")
    @patch("generators.rikishi.ShusshinGenerator.get")
    @patch("base.models.GameDate.objects.current")
    def test_get(self, mock_current, mock_shusshin_get, mock_name_get):
        mock_name_get.return_value = ("Test Name", "テストネーム")
        mock_shusshin_get.return_value = Shusshin(
            country="JP", prefecture="Tokyo"
        )
        mock_current.return_value = GameDate(2023, 1, 1)

        rikishi, stats = self.generator.get()

        self.assertEqual(rikishi.name, "Test Name")
        self.assertEqual(rikishi.name_jp, "テストネーム")
        self.assertIsInstance(rikishi.shusshin, Shusshin)
        self.assertEqual(rikishi.shusshin.country, "JP")
        self.assertEqual(rikishi.shusshin.prefecture, "Tokyo")
        self.assertEqual(rikishi.debut, GameDate(2023, 1, 1))
        self.assertIsInstance(stats, RikishiStats)
        self.assertEqual(stats.rikishi, rikishi)

    def test_get_potential_ability(self):
        potential = self.generator.get_potential_ability()
        self.assertTrue(MIN_POTENTIAL <= potential <= MAX_POTENTIAL)

    def test_get_current_ability(self):
        potential = AVG_POTENTIAL
        current = self.generator.get_current_ability(potential)
        self.assertTrue(MIN_POTENTIAL <= current <= potential / 2)

    @patch.object(
        RikishiGenerator, "get_potential_ability", return_value=AVG_POTENTIAL
    )
    @patch.object(
        RikishiGenerator, "get_current_ability", return_value=MIN_POTENTIAL
    )
    def test_get_stats(
        self, mock_get_current_ability, mock_get_potential_ability
    ):
        rikishi = Rikishi(
            name="Test",
            name_jp="テスト",
            shusshin=Shusshin(country="JP", prefecture="Tokyo"),
            debut=GameDate(2023, 1, 1),
        )
        stats = self.generator.get_stats(rikishi)
        self.assertEqual(stats.potential, AVG_POTENTIAL)
        self.assertEqual(stats.rikishi, rikishi)


if __name__ == "__main__":
    unittest.main()
