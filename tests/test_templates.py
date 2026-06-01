from pathlib import Path
import unittest

from oss_maintainer_toolbelt.templates import lint_issue_templates


class TemplateLintTests(unittest.TestCase):
    def test_lint_issue_templates_accepts_complete_template(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir) / ".github" / "ISSUE_TEMPLATE"
            directory.mkdir(parents=True)
            (directory / "bug.md").write_text(
                "---\nname: Bug report\nabout: Report a bug\ntitle: \"[Bug]: \"\nlabels: bug\n---\n\n## What happened?\n",
                encoding="utf-8",
            )

            result = lint_issue_templates(directory)

        self.assertEqual(result["problems"], [])
        self.assertEqual(result["checked"], 1)

    def test_lint_issue_templates_reports_missing_front_matter(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir) / ".github" / "ISSUE_TEMPLATE"
            directory.mkdir(parents=True)
            (directory / "bug.md").write_text("## What happened?\n", encoding="utf-8")

            result = lint_issue_templates(directory)

        self.assertTrue(result["problems"])


if __name__ == "__main__":
    unittest.main()
