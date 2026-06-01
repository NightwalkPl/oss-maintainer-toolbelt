from pathlib import Path
import unittest

from oss_maintainer_toolbelt.envcheck import compare_env_files


class EnvCheckTests(unittest.TestCase):
    def test_compare_env_files_reports_missing_keys(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            example = root / ".env.example"
            actual = root / ".env"
            example.write_text("API_KEY=\nexport DATABASE_URL=\n", encoding="utf-8")
            actual.write_text("API_KEY=abc\nLOCAL_ONLY=true\n", encoding="utf-8")

            result = compare_env_files(example, actual)

        self.assertEqual(result["missing"], ["DATABASE_URL"])
        self.assertEqual(result["extra"], ["LOCAL_ONLY"])


if __name__ == "__main__":
    unittest.main()
