import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import GameDate


class AlphaIDFieldTestCase(TestCase):
    def test_alpha_id_generation(self):
        user = get_user_model().objects.create(username="testuser")

        # Check if the AlphaIDField generates a unique alpha ID
        self.assertIsNotNone(user.id)
        self.assertEqual(len(user.id), 16)


class GameDateTestCase(TestCase):
    def test_game_month_creation(self):
        game_month = GameDate.objects.create(year=2023, month=1, day=1)

        # Check if the ID is correctly generated
        self.assertEqual(game_month.id, "2023-01-01")

    def test_game_date_current(self):
        GameDate.objects.create(year=2023, month=1, day=1)

        current_date = GameDate.objects.current()

        # Check if the current date is returned
        self.assertEqual(current_date.id, "2023-01-01")

    def test_game_date_tick(self):
        GameDate.objects.create(year=2023, month=1, day=1)

        GameDate.objects.tick()

        # Check if tick created a new date
        new_game_date = GameDate.objects.last()
        self.assertEqual(new_game_date.year, 2023)
        self.assertEqual(new_game_date.month, 1)
        self.assertEqual(new_game_date.day, 2)
        self.assertEqual(new_game_date.id, "2023-01-02")

    def test_game_date_new_month(self):
        GameDate.objects.create(year=2023, month=1, day=24)

        GameDate.objects.tick()

        # Check if month increases
        new_game_date = GameDate.objects.last()
        self.assertEqual(new_game_date.year, 2023)
        self.assertEqual(new_game_date.month, 2)
        self.assertEqual(new_game_date.day, 1)
        self.assertEqual(new_game_date.id, "2023-02-01")

    def test_game_date_new_year(self):
        GameDate.objects.create(year=2023, month=12, day=24)

        GameDate.objects.tick()

        # Check if year increases
        new_game_date = GameDate.objects.last()
        self.assertEqual(new_game_date.year, 2024)
        self.assertEqual(new_game_date.month, 1)
        self.assertEqual(new_game_date.day, 1)
        self.assertEqual(new_game_date.id, "2024-01-01")

    def test_create_default_game_date(self):
        GameDate.objects.tick()

        # Check if a default GameDate is created if none exist in DB
        default_game_date = GameDate.objects.last()
        self.assertEqual(default_game_date.year, 1)
        self.assertEqual(default_game_date.month, 1)
        self.assertEqual(default_game_date.id, "0001-01-01")

    def test_game_date_str(self):
        game_date = GameDate.objects.create(year=2023, month=3, day=14)

        # Check if the __str__ method returns the expected string
        self.assertEqual(str(game_date), "2023-03-14")


if __name__ == "__main__":
    unittest.main()
