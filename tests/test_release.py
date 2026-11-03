import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_release.py"
spec = importlib.util.spec_from_file_location("release_check", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReleaseBehavior(unittest.TestCase):
    def make_package(self, root, content="Public demo"):
        (root / "README.md").write_text(content)
        (root / "release-manifest.json").write_text(json.dumps({"files": ["README.md", "release-manifest.json"]}))

    def test_extra_file_blocks_release(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_package(root)
            (root / "unlisted.csv").write_text("should not ship")
            with self.assertRaises(ValueError):
                module.verify(root)

    def test_symlink_cannot_import_external_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_package(root)
            (root / "external").symlink_to(root / "README.md")
            with self.assertRaises(ValueError):
                module.verify(root)

    def test_personal_path_blocks_release(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            # Build the test input without embedding a personal path in this source.
            self.make_package(root, "/" + "Users" + "/" + "example-person" + "/notes.txt")
            with self.assertRaises(ValueError):
                module.verify(root)

    def test_expected_public_files_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_package(root)
            self.assertEqual(module.verify(root), 2)


if __name__ == "__main__":
    unittest.main()
