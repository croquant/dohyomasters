import unittest

from .alpha_id import alpha_id


class TestAlphaId(unittest.TestCase):
    def test_generate_unique_ids(self):
        # Generate 10000 alpha IDs
        num_ids = 10000
        generated_ids = set()
        for _ in range(num_ids):
            generated_ids.add(alpha_id())

        # Check if all generated IDs have length 16
        for generated_id in generated_ids:
            self.assertEqual(len(generated_id), 16)

        # Check if there are no duplicate IDs
        self.assertEqual(len(generated_ids), num_ids)


if __name__ == "__main__":
    unittest.main()
