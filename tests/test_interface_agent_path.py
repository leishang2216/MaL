import json
import unittest
from pathlib import Path

import jsonc


class InterfaceAgentPathTest(unittest.TestCase):
    def test_interface_uses_dev_agent_path_and_exposes_wait_mode_options(self):
        root = Path(__file__).resolve().parent.parent
        interface_path = root / "assets" / "interface.json"
        interface = jsonc.loads(interface_path.read_text(encoding="utf-8"))
        wait_mode = interface["option"]["向阳花等待模式"]
        bow_no_case = next(case for case in interface["option"]["向阳花是否为鞠躬号"]["cases"] if case["name"] == "No")

        self.assertIn("agent", interface)
        self.assertEqual(interface["agent"]["child_exec"], "python")
        self.assertEqual(interface["agent"]["child_args"], ["../agent/main.py"])
        self.assertTrue((root / "agent" / "main.py").is_file())
        self.assertIn("向阳花等待模式", interface["option"])
        self.assertIn("向阳花固定等待", interface["option"])
        self.assertIn("向阳花随机等待", interface["option"])
        self.assertEqual(wait_mode["type"], "select")
        self.assertEqual(interface["task"][0]["entry"], "Sunflower_LoopEntry")
        self.assertIn("向阳花等待模式", interface["task"][0]["option"])
        self.assertEqual(
            bow_no_case["pipeline_override"]["Sunflower_BowAccountGate"]["next"],
            "Sunflower_WaitBySetting",
        )
        bow_yes_case = next(case for case in interface["option"]["向阳花是否为鞠躬号"]["cases"] if case["name"] == "Yes")
        self.assertEqual(
            bow_yes_case["pipeline_override"]["Sunflower_BowAccountGate"]["next"],
            "Sunflower_Stage2_Entry",
        )
        fixed_case = next(case for case in wait_mode["cases"] if case["name"] == "固定秒数")
        random_case = next(case for case in wait_mode["cases"] if case["name"] == "随机区间")
        self.assertIn("option", fixed_case)
        self.assertIn("option", random_case)
        self.assertIn("向阳花固定等待", fixed_case["option"])
        self.assertIn("向阳花随机等待", random_case["option"])

    def test_pipeline_uses_refactored_stage_flow_and_custom_wait(self):
        pipeline_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "resource"
            / "pipeline"
            / "sunflower_task.json"
        )
        pipeline = json.loads(pipeline_path.read_text(encoding="utf-8"))
        loop_entry = pipeline["Sunflower_LoopEntry"]
        stage1_page_check = pipeline["Sunflower_Stage1_PageCheck"]
        bow_gate = pipeline["Sunflower_BowAccountGate"]
        stage2_entry = pipeline["Sunflower_Stage2_Entry"]
        stage2_page_check = pipeline["Sunflower_Stage2_PageCheck"]
        wait_node = pipeline["Sunflower_WaitBySetting"]

        self.assertEqual(
            loop_entry["next"],
            ["Sunflower_Stage1_PageCheck", "Sunflower_Stage1_ActionEntry"],
        )
        self.assertEqual(
            pipeline["Sunflower_Stage1_ActionEntry"]["next"],
            "Sunflower_Stage1_ClickDynamic_1",
        )
        self.assertEqual(stage1_page_check["next"], "Sunflower_BowAccountGate")
        self.assertEqual(pipeline["Sunflower_Stage1_FinalLongPress"]["next"], "Sunflower_BowAccountGate")
        self.assertEqual(bow_gate["next"], "Sunflower_WaitBySetting")
        self.assertEqual(stage2_entry["next"], ["Sunflower_Stage2_PageCheck"])
        self.assertEqual(stage2_entry["on_error"], "Sunflower_LoopEntry")
        self.assertEqual(stage2_page_check["next"], "Sunflower_Stage3_ClickFixed")
        self.assertEqual(wait_node["action"], "Custom")
        self.assertEqual(wait_node["custom_action"], "sunflower_wait")
        self.assertEqual(wait_node["custom_action_param"]["mode"], "fixed")
        self.assertEqual(wait_node["next"], "Sunflower_LoopEntry")


if __name__ == "__main__":
    unittest.main()
