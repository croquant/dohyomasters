import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import GameMonth


class AlphaIDFieldTestCase(TestCase):
    def test_alpha_id_generation(self):
        user = get_user_model().objects.create(username="testuser")

        # Check if the AlphaIDField generates a unique alpha ID
        self.assertIsNotNone(user.id)
        self.assertEqual(len(user.id), 16)


class GameMonthTestCase(TestCase):
    def test_game_month_creation(self):
        game_month = GameMonth.objects.create(year=2023, number=1)

        # Check if the ID is correctly generated
        self.assertEqual(game_month.id, "2023-1")

    def test_game_month_tick(self):
        GameMonth.objects.create(year=2023, number=1)

        GameMonth.objects.tick()

        # Check if tick created a new month
        new_game_month = GameMonth.objects.last()
        self.assertEqual(new_game_month.year, 2023)
        self.assertEqual(new_game_month.number, 2)
        self.assertEqual(new_game_month.id, "2023-2")

    def test_game_month_new_year(self):
        GameMonth.objects.create(year=2023, number=12)

        GameMonth.objects.tick()

        # Check if year increases and month is reset to 1 after month number 12
        new_game_month = GameMonth.objects.last()
        self.assertEqual(new_game_month.year, 2024)
        self.assertEqual(new_game_month.number, 1)
        self.assertEqual(new_game_month.id, "2024-1")

    def test_create_default_game_month(self):
        GameMonth.objects.tick()

        # Check if a default GameMonth is created if none exist in DB
        default_game_month = GameMonth.objects.last()
        self.assertEqual(default_game_month.year, 1)
        self.assertEqual(default_game_month.number, 1)
        self.assertEqual(default_game_month.id, "1-1")

    def test_game_month_str(self):
        game_month = GameMonth.objects.create(year=2023, number=3)

        # Check if the __str__ method returns the expected string
        self.assertEqual(str(game_month), "2023-03")


if __name__ == "__main__":
    unittest.main()
