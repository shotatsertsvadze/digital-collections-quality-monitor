
# Digital Collections Quality Monitor

A learning-driven Python project focused on metadata quality assurance and digitization workflows in academic libraries.

## Project Goals

- Explore bibliographic metadata and digital collections.
- Learn Python for data processing and validation.
- Work with XML, MODS, METS, ALTO and IIIF.
- Explore OCR/HTR quality assurance.
- Generate automated data quality reports.

## Planned Technologies

- Python
- XML, JSON, CSV
- OpenRefine
- Catmandu
- IIIF APIs
- Git and GitHub

## Current Status

🚧 Work in progress — initial project setup.

This project is being developed step by step as part of my professional development in library data management and digitization.

## Learning Approach

Each implementation step will be documented with Git commits. The goal is to build and understand the functionality progressively, rather than presenting an artificially completed project.



## Data Source

This project uses publicly accessible IIIF metadata from the
Staatsbibliothek zu Berlin (Berlin State Library).

Sample object: PPN867445300

IIIF Manifest:
https://content.staatsbibliothek-berlin.de/dc/PPN867445300/manifest

The source manifest follows IIIF Presentation API 2.

Raw source data is downloaded locally and is not committed
to this repository.

## Running the IIIF Quality Checks

Requirements: Python 3.13 (standard library only).

Download the sample manifest:

```bash
mkdir -p data/raw

curl -fL \
  https://content.staatsbibliothek-berlin.de/dc/PPN867445300/manifest \
  -o data/raw/PPN867445300_manifest.json
```

Run the validator:

```bash
python3 src/check_iiif.py
```

## Initial Validation Results

Sample: PPN867445300
Checked: November 2026

| Quality Check | Result |
|---|---:|
| Total canvases | 426 |
| Canvases without first image URL | 0 |
| Missing canvas IDs | 0 |
| Duplicate canvas IDs | 0 |
| Invalid canvas dimensions | 0 |

No issues were detected by the implemented checks.

## Current Limitations

- Checks only the first image entry per canvas.
- Does not verify whether image URLs are accessible.
- Does not yet validate the complete IIIF specification.
- Does not yet compare IIIF with METS/MODS or OCR metadata.
- Results are based on one sample manifest.

## Next Steps

- Improve IIIF validation and automated tests.
- Analyze METS/MODS and ALTO XML metadata.
- Compare metadata across formats.
- Generate structured quality reports.
- Evaluate multiple digitized objects.



## Cross-Format Consistency Validation

The project compares IIIF Presentation API 2 manifests with
METS XML metadata to identify inconsistencies in digitized
library collections.

### Validation checks

- IIIF Canvas count vs. METS physical page count
- Canvas numbering and METS page order
- METS physical page identifiers
- Image identifier consistency between IIIF image resources
  and METS DEFAULT file references

### Results

Tested with a publicly accessible digitized object from
the Staatsbibliothek zu Berlin (PPN867445300):

- IIIF Canvases: 426
- METS physical pages: 426
- Sequence inconsistencies: 0
- Image identifier mismatches: 0

### Run the validator

Using the included synthetic test fixtures:

```bash
python3 src/check_cross_format.py \
  tests/fixtures/iiif_valid.json \
  tests/fixtures/mets_cross_valid.xml
```

### Automated tests

```bash
python3 -m unittest discover -s tests -v
```

Current test suite: 4 tests covering valid and invalid
METS references and IIIF/METS image identifiers.

### Limitations

- Image identifiers are compared using URL patterns.
- Image contents and HTTP availability are not verified.
- Full IIIF/METS schema validation is not implemented.
- The synthetic METS fixtures are simplified and are
  not intended as complete schema-valid METS documents.
```



## OCR Quality Monitoring (ALTO XML)

This module analyzes ALTO XML files from digitized
library collections and generates a CSV quality report.

### Features

- Counts OCR text units, text lines, and illustrations
- Flags pages with missing or very little OCR text
- Generates a structured CSV report
- Supports configurable input and output paths

### Usage

Run the OCR analyzer:

    python3 src/check_ocr.py data/raw reports/ocr_quality_report.csv

Run automated tests:

    python3 -m unittest discover -s tests -v

### Sample Results

Four ALTO XML pages from Staatsbibliothek zu Berlin
(PPN867445300) were analyzed.

- Pages analyzed: 4
- OCR text units: 580
- Pages flagged for review: 3
- Pages with text detected: 1

### Limitations

The module checks OCR text presence, not recognition
accuracy. Pages with little text are flagged for manual
review, not automatically classified as errors.

The five-unit review threshold is experimental.
