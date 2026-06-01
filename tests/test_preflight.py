from pathlib import Path
import subprocess
import tempfile
import unittest

from oss_maintainer_toolbelt.preflight import build_preflight_checklist


class PreflightTests(unittest.TestCase):
    def test_preflight_builds_release_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "-C", str(root), "init", "-b", "main"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")
            (root / ".omt.json").write_text(
                '{"required_docs": ["README.md"], "issue_template_path": ".github/ISSUE_TEMPLATE"}',
                encoding="utf-8",
            )
            template_dir = root / ".github" / "ISSUE_TEMPLATE"
            template_dir.mkdir(parents=True)
            (template_dir / "bug.md").write_text(
                "---\nname: Bug\nabout: Bug\ntitle: \"[Bug]: \"\nlabels: bug\n---\n\n## Details\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "feat: add example"], check=True, capture_output=True)

            result = build_preflight_checklist(root)

        self.assertTrue(result["passed"])
        self.assertIn("# Pre-release Checklist", result["markdown"])
        self.assertIn("## Changelog Draft", result["markdown"])


if __name__ == "__main__":
    unittest.main()

