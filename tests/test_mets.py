
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestMetsValidator(unittest.TestCase):

    def test_detects_broken_structural_link(self):
        result = subprocess.run(
            [
                sys.executable,
                "src/check_mets.py",
                "tests/fixtures/invalid_mets.xml",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertIn("Broken structural links: 1", result.stdout)
        self.assertIn("PHYS_9999", result.stdout)

    def test_accepts_valid_structural_link(self):
        result = subprocess.run(
            [
                sys.executable,
                "src/check_mets.py",
                "tests/fixtures/valid_mets.xml",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertIn("Broken structural links: 0", result.stdout)


if __name__ == "__main__":
    unittest.main()
