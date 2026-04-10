import unittest
from pathlib import Path


class InterfaceAgentPathTest(unittest.TestCase):
    def test_agent_entry_uses_project_dir_placeholder(self):
        interface_path = Path(__file__).resolve().parent.parent / "assets" / "interface.json"
        content = interface_path.read_text(encoding="utf-8")

        self.assertIn('"{PROJECT_DIR}/agent/main.py"', content)


if __name__ == "__main__":
    unittest.main()
