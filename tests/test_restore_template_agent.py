import importlib.util
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import jsonc


class RestoreTemplateAgentTest(unittest.TestCase):
    def test_template_agent_files_exist(self):
        root = Path(__file__).resolve().parent.parent

        self.assertTrue((root / "agent" / "main.py").is_file())
        self.assertTrue((root / "agent" / "sunflower_actions.py").is_file())

    def test_interface_agent_path_is_valid_relative_to_interface_directory(self):
        root = Path(__file__).resolve().parent.parent
        interface_path = root / "assets" / "interface.json"
        interface = jsonc.loads(interface_path.read_text(encoding="utf-8"))
        agent_entry = (root / "assets" / interface["agent"]["child_args"][0]).resolve()

        self.assertEqual(interface["agent"]["child_args"], ["../agent/main.py"])
        self.assertTrue(agent_entry.is_file())

    def test_install_resource_copies_agent_and_rewrites_path_for_package(self):
        root = Path(__file__).resolve().parent.parent
        install_module = self._load_install_module(root)

        with TemporaryDirectory() as temp_dir:
            install_module.install_path = Path(temp_dir) / "install"
            install_module.configure_ocr_model = lambda: None

            install_module.install_resource()

            interface = jsonc.loads(
                (install_module.install_path / "interface.json").read_text(encoding="utf-8")
            )

            self.assertEqual(interface["agent"]["child_args"], ["./agent/main.py"])
            self.assertTrue((install_module.install_path / "agent" / "main.py").is_file())
            self.assertTrue((install_module.install_path / "agent" / "sunflower_actions.py").is_file())

    def _load_install_module(self, root: Path):
        module_path = root / "tools" / "install.py"
        original_argv = sys.argv[:]
        original_path = sys.path[:]

        try:
            sys.argv = [str(module_path), "v0.0.1", "win", "x86_64"]
            sys.path.insert(0, str(module_path.parent))
            spec = importlib.util.spec_from_file_location("install_module_for_test", module_path)
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
            return module
        finally:
            sys.argv = original_argv
            sys.path = original_path


if __name__ == "__main__":
    unittest.main()
