import random
import unittest

from agent.my_action import compute_wait_seconds


class ComputeWaitSecondsTest(unittest.TestCase):
    def test_returns_fixed_seconds_in_fixed_mode(self):
        seconds = compute_wait_seconds(
            {
                "mode": "fixed",
                "fixed_seconds": 8,
            }
        )

        self.assertEqual(seconds, 8)

    def test_returns_random_seconds_in_random_mode(self):
        generator = random.Random(1234)

        seconds = compute_wait_seconds(
            {
                "mode": "random",
                "min_seconds": 3,
                "max_seconds": 9,
            },
            generator=generator,
        )

        self.assertEqual(seconds, 9)

    def test_swaps_invalid_random_range(self):
        generator = random.Random(1234)

        seconds = compute_wait_seconds(
            {
                "mode": "random",
                "min_seconds": 9,
                "max_seconds": 3,
            },
            generator=generator,
        )

        self.assertTrue(3 <= seconds <= 9)


if __name__ == "__main__":
    unittest.main()
