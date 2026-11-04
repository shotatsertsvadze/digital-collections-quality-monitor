
import csv
import sys
from pathlib import Path
from collections import Counter
import xml.etree.ElementTree as ET


# 1. Input directory

input_dir = (
    Path(sys.argv[1])
    if len(sys.argv) > 1
    else Path("data/raw")
)

ocr_files = sorted(input_dir.glob("page_*_ocr.xml"))

if not ocr_files:
    raise SystemExit(
        f"No OCR XML files found in {input_dir}"
    )


# 2. Analyze OCR files

results = []

for path in ocr_files:
    root = ET.parse(path).getroot()

    counts = Counter(
        element.tag.split("}")[-1]
        for element in root.iter()
    )

    word_count = sum(
        1
        for element in root.iter()
        if element.tag.split("}")[-1] == "String"
        and element.get("CONTENT")
    )

    # Experimental review threshold

    if word_count == 0:
        status = "REVIEW"
        reason = "No OCR text"

    elif word_count < 5:
        status = "REVIEW"
        reason = "Very little OCR text"

    else:
        status = "TEXT PRESENT"
        reason = "Text detected"

    results.append({
        "file": path.name,
        "words": word_count,
        "text_lines": counts["TextLine"],
        "illustrations": counts["Illustration"],
        "status": status,
        "reason": reason,
    })


# 3. Print individual results

print("\nOCR QUALITY REPORT")
print("=" * 50)

for result in results:
    print(f"\nFile: {result['file']}")
    print(f"Strings: {result['words']}")
    print(f"Text lines: {result['text_lines']}")
    print(f"Illustrations: {result['illustrations']}")
    print(f"Status: {result['status']}")
    print(f"Reason: {result['reason']}")


# 4. Calculate summary statistics

review_count = sum(
    1 for result in results
    if result["status"] == "REVIEW"
)

pages_with_ocr_text = sum(
    1 for result in results
    if result["words"] > 0
)

pages_meeting_threshold = sum(
    1 for result in results
    if result["words"] >= 5
)

total_ocr_strings = sum(
    result["words"] for result in results
)


# 5. Print summary

print("\nSUMMARY")
print("=" * 50)

print("Pages analyzed:", len(results))
print("Pages for review:", review_count)
print("Pages containing OCR text:", pages_with_ocr_text)
print("Pages meeting text threshold:", pages_meeting_threshold)
print("Total OCR strings:", total_ocr_strings)


# 6. Export results to CSV

output_path = (
    Path(sys.argv[2])
    if len(sys.argv) > 2
    else Path("reports/ocr_quality_report.csv")
)

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

fieldnames = [
    "file",
    "words",
    "text_lines",
    "illustrations",
    "status",
    "reason",
]

with output_path.open(
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    writer = csv.DictWriter(
        csv_file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(results)

print("\nCSV report saved:", output_path)
