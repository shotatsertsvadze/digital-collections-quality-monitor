
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evaluate_ocr import evaluate_text


class TestOCRAccuracy(unittest.TestCase):

    def test_verified_ground_truth(self):
        fixture_path = ROOT / "tests/fixtures/ocr_accuracy_case.json"

        with fixture_path.open(encoding="utf-8") as file:
            case = json.load(file)

        result = evaluate_text(
            case["ground_truth"],
            case["ocr_text"]
        )

        self.assertEqual(
            result["character_errors"],
            case["expected_character_errors"]
        )

        self.assertEqual(
            result["word_errors"],
            case["expected_word_errors"]
        )

        self.assertAlmostEqual(
            result["cer"],
            case["expected_cer"]
        )

        self.assertAlmostEqual(
            result["wer"],
            case["expected_wer"]
        )

    def test_perfect_ocr(self):
        text = "Welt im Bild"

        result = evaluate_text(text, text)

        self.assertEqual(result["cer"], 0)
        self.assertEqual(result["wer"], 0)

    
    def test_empty_ground_truth(self):
        with self.assertRaises(ValueError):
            evaluate_text("", "Welt im Bild")



if __name__ == "__main__":
    unittest.main()
