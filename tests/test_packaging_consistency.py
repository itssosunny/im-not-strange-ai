from __future__ import annotations

import filecmp
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_REFERENCES = (
    PROJECT_ROOT / ".claude" / "skills" / "im-not-strange-ai" / "references"
)
CODEX_REFERENCES = (
    PROJECT_ROOT / "codex-plugin" / "skills" / "im-not-strange-ai" / "references"
)


def _source_files(root: Path) -> set[Path]:
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    }


class PackagingConsistencyTests(unittest.TestCase):
    def test_codex_references_match_claude_references(self) -> None:
        self.assertTrue(CLAUDE_REFERENCES.is_dir())
        self.assertTrue(CODEX_REFERENCES.is_dir())

        claude_files = _source_files(CLAUDE_REFERENCES)
        codex_files = _source_files(CODEX_REFERENCES)
        self.assertEqual(claude_files, codex_files)

        for rel_path in sorted(claude_files):
            with self.subTest(path=str(rel_path)):
                self.assertTrue(
                    filecmp.cmp(
                        CLAUDE_REFERENCES / rel_path,
                        CODEX_REFERENCES / rel_path,
                        shallow=False,
                    )
                )
