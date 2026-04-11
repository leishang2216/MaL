import importlib.util
import unittest
from pathlib import Path


def load_sunflower_actions_module():
    root = Path(__file__).resolve().parent.parent
    module_path = root / "agent" / "sunflower_actions.py"
    spec = importlib.util.spec_from_file_location("sunflower_actions_for_test", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SunflowerActionTest(unittest.TestCase):
    def test_fixed_mode_returns_fixed_seconds(self):
        module = load_sunflower_actions_module()

        seconds = module.resolve_wait_seconds(
            {
                "mode": "fixed",
                "fixed_seconds": 12,
            }
        )

        self.assertEqual(seconds, 12)

    def test_random_mode_returns_value_inside_range(self):
        module = load_sunflower_actions_module()

        seconds = module.resolve_wait_seconds(
            {
                "mode": "random",
                "random_min_seconds": 3,
                "random_max_seconds": 7,
            },
            randint_func=lambda start, end: 5,
        )

        self.assertEqual(seconds, 5)

    def test_random_mode_rejects_reversed_range(self):
        module = load_sunflower_actions_module()

        with self.assertRaises(ValueError):
            module.resolve_wait_seconds(
                {
                    "mode": "random",
                    "random_min_seconds": 8,
                    "random_max_seconds": 2,
                }
            )


if __name__ == "__main__":
    unittest.main()
