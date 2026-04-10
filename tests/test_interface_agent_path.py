import json
import unittest
from pathlib import Path

import jsonc


class InterfaceAgentPathTest(unittest.TestCase):
    def test_interface_removes_agent_and_random_wait_options(self):
        interface_path = Path(__file__).resolve().parent.parent / "assets" / "interface.json"
        interface = jsonc.loads(interface_path.read_text(encoding="utf-8"))
        no_case = next(
            case for case in interface["option"]["向阳花是否为鞠躬号"]["cases"] if case["name"] == "No"
        )

        self.assertNotIn("agent", interface)
        self.assertNotIn("向阳花等待模式", interface["option"])
        self.assertNotIn("向阳花随机等待", interface["option"])
        self.assertEqual(interface["task"][0]["entry"], "Sunflower_LoopEntry")
        self.assertEqual(
            no_case["pipeline_override"]["Sunflower_Stage1_PageCheck"]["next"],
            "Sunflower_WaitBySetting",
        )
        self.assertEqual(
            no_case["pipeline_override"]["Sunflower_Stage1_FinalLongPress"]["next"],
            "Sunflower_WaitBySetting",
        )

    def test_pipeline_wait_node_uses_builtin_delay(self):
        pipeline_path = (
            Path(__file__).resolve().parent.parent / "assets" / "resource" / "pipeline" / "my_task.json"
        )
        pipeline = json.loads(pipeline_path.read_text(encoding="utf-8"))
        loop_entry = pipeline["Sunflower_LoopEntry"]
        wait_node = pipeline["Sunflower_WaitBySetting"]

        self.assertEqual(
            loop_entry["next"],
            ["Sunflower_Stage1_PageCheck", "Sunflower_Stage1_Fallback"],
        )
        self.assertEqual(
            pipeline["Sunflower_Stage1_Fallback"]["next"],
            "Sunflower_Stage1_ClickDynamic_1",
        )
        self.assertEqual(wait_node["action"], "DoNothing")
        self.assertNotIn("custom_action", wait_node)
        self.assertIn("post_delay", wait_node)
        self.assertEqual(wait_node["next"], "Sunflower_LoopEntry")


if __name__ == "__main__":
    unittest.main()
