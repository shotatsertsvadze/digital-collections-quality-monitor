
# Digital Collections Quality Monitor

A learning-driven Python project focused on metadata quality assurance and digitization workflows in academic libraries.

## Project Goals

- Explore bibliographic metadata and digital collections.
- Learn Python for data processing and validation.
- Work with XML, MODS, METS, ALTO and IIIF.
- Explore OCR/HTR quality assurance.
- Generate automated data quality reports.


## Technologies

**Implemented in this project:**

- Python 3 (standard library)
- XML parsing with ElementTree
- JSON and CSV processing
- IIIF Presentation API 2
- METS XML
- ALTO XML for OCR data
- Levenshtein edit distance for CER/WER
- Automated testing with unittest
- Git and GitHub

**Related learning topics:**

- Dublin Core and MODS
- OpenRefine
- Catmandu
- OCR/HTR workflows



## Project Status

**Status: Functional MVP implemented and tested.**

The project currently includes:

- CSV metadata checks for missing titles and duplicate IDs
- IIIF Canvas and image-reference checks
- METS structural reference validation
- Cross-format consistency checks between IIIF and METS
- ALTO OCR text-presence analysis
- CSV export of OCR quality indicators
- OCR accuracy evaluation using CER and WER
- Automated tests using synthetic fixtures

The automated test suite has been verified in a fresh
clone of the repository.

This is an independent learning and portfolio project,
not an official quality assurance system of the
Staatsbibliothek zu Berlin.


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


## Scope and Limitations

- The IIIF checker examines selected structural properties,
  not the complete IIIF specification.
- The METS checker validates selected references,
  not full METS schema compliance.
- Cross-format checks compare identifiers and page order
  using patterns observed in the sample object.
- Image contents and HTTP availability are not verified.
- OCR monitoring measures text presence, not recognition
  accuracy.
- CER/WER accuracy measurements require manually verified
  Ground Truth.
- Results are based on a limited sample of digitized material.



## Potential Future Improvements

- Validate additional digitized objects and data formats.
- Improve error handling for malformed or incomplete files.
- Add broader automated test coverage.
- Introduce more configurable validation rules.
- Evaluate larger, manually verified OCR samples.
- Add automated CI checks with GitHub Actions.

These are possible extensions beyond the current MVP.




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
- Pages containing OCR text: 2
- Pages meeting experimental threshold (5 or more strings): 1

### Limitations

The module checks OCR text presence, not recognition
accuracy. Pages with little text are flagged for manual
review, not automatically classified as errors.

The five-unit review threshold is experimental.



## OCR Accuracy Evaluation (CER / WER)

The project includes an experimental Python-based
OCR accuracy evaluator using Levenshtein edit distance.

It calculates:

- Character Error Rate (CER)
- Word Error Rate (WER)

### Verified Ground Truth Example

Source: *Welt im Bild* (1918), digital page 20.  
Identifier: PPN867445300.

**Ground Truth (manually verified):**

> Deutscher Fesselballon zur Beobachtung

**OCR Output (ALTO XML):**

> Deutscher Fesselballon jur Beobachtung

**Results:**

| Metric | Result |
|---|---:|
| Character errors | 1 |
| Word errors | 1 |
| CER | 2.63% |
| WER | 25.00% |

The results apply only to this four-word excerpt,
not to the complete digitized page.

### Run

    python3 src/evaluate_ocr.py

### Automated Testing

    python3 -m unittest discover -s tests -v

### Limitations

- Accuracy evaluation requires verified Ground Truth.
- No full-page OCR accuracy benchmark is provided.
- The example is not a representative sample of the collection.
- Text normalization policies are not yet implemented.
