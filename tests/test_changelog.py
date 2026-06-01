import unittest

from oss_maintainer_toolbelt.changelog import COMMIT_RE


class ChangelogTests(unittest.TestCase):
    def test_conventional_commit_parser_supports_scope_and_breaking_marker(self) -> None:
        match = COMMIT_RE.match("feat(cli)!: add repository report command")

        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match.group("type"), "feat")
        self.assertEqual(match.group("breaking"), "!")
        self.assertEqual(match.group("text"), "add repository report command")


if __name__ == "__main__":
    unittest.main()
