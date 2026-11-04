import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestOCRValidator(unittest.TestCase):

    def run_check(self, words):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            xml_path = folder / "page_0001_ocr.xml"
            report_path = folder / "report.csv"

            strings = "".join(
                f'<String CONTENT="word{i}"/>'
                for i in range(words)
            )

            xml_path.write_text(
                f"<alto><TextLine>{strings}</TextLine></alto>",
                encoding="utf-8"
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "src/check_ocr.py",
                    str(folder),
                    str(report_path),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=result.stderr
            )

            with report_path.open(
                encoding="utf-8",
                newline=""
            ) as file:
                return list(csv.DictReader(file))

    def test_text_present(self):
        rows = self.run_check(10)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["words"], "10")
        self.assertEqual(rows[0]["status"], "TEXT PRESENT")

    def test_no_ocr_text(self):
        rows = self.run_check(0)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["words"], "0")
        self.assertEqual(rows[0]["status"], "REVIEW")

    
    def test_empty_ocr_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                [
                    sys.executable,
                    "src/check_ocr.py",
                    temp,
                    str(Path(temp) / "report.csv"),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn(
                "No OCR XML files found",
                result.stderr
            )



if __name__ == "__main__":
    unittest.main()
