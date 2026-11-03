
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestCrossFormatValidator(unittest.TestCase):

    def run_validator(self, manifest_name):
        return subprocess.run(
            [
                sys.executable,
                "src/check_cross_format.py",
                f"tests/fixtures/{manifest_name}",
                "tests/fixtures/mets_cross_valid.xml",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def test_valid_image_identifiers(self):
        result = self.run_validator("iiif_valid.json")

        self.assertEqual(result.returncode, 0)
        self.assertIn(
            "IIIF / METS Image Identifier Check",
            result.stdout
        )
        self.assertIn("Issues found: 0", result.stdout)

    def test_invalid_image_identifier(self):
        result = self.run_validator("iiif_invalid.json")

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "Page 1: image identifier mismatch",
            result.stdout
        )


if __name__ == "__main__":
    unittest.main()
