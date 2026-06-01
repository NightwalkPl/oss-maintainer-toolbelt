from pathlib import Path
import tempfile
import unittest

from oss_maintainer_toolbelt.report import build_repo_report


class ReportTests(unittest.TestCase):
    def test_report_uses_configured_required_docs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")
            (root / ".omt.json").write_text('{"required_docs": ["README.md", "SECURITY.md"]}', encoding="utf-8")

            result = build_repo_report(root)

        self.assertEqual(result["present_docs"], ["README.md"])
        self.assertEqual(result["missing_docs"], ["SECURITY.md"])
        self.assertIn("# Repository Maintenance Report", result["markdown"])


if __name__ == "__main__":
    unittest.main()

