import sys
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path

# Load IIIF Manifest
manifest_path = (
    Path(sys.argv[1])
    if len(sys.argv) > 1
    else Path("data/raw/PPN867445300_manifest.json")
)
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
canvases = manifest["sequences"][0]["canvases"]

# Load METS XML

mets_path = (
    Path(sys.argv[2])
    if len(sys.argv) > 2
    else Path("data/raw/PPN867445300_mets.xml")
)

root = ET.parse(mets_path).getroot()

ns = {"mets": "http://www.loc.gov/METS/"}

physical_map = root.find(".//mets:structMap[@TYPE='PHYSICAL']", ns)
pages = physical_map.findall(".//mets:div[@TYPE='page']", ns)

print("IIIF Canvases:", len(canvases))
print("METS Pages:", len(pages))

# Inspect the first three records
for i in range(min(3, len(canvases), len(pages))):
    canvas = canvases[i]
    page = pages[i]

    fptr = page.find("mets:fptr", ns)

    print(f"\nPosition {i + 1}")
    print("IIIF Canvas ID:", canvas.get("@id"))
    print("METS Page ID:", page.get("ID"))
    print("METS Order:", page.get("ORDER"))
    print("METS FILEID:", fptr.get("FILEID") if fptr is not None else None)

# Check sequence consistency across all pages

issues = []

if len(canvases) != len(pages):
    issues.append("Different numbers of canvases and pages")

for position, (canvas, page) in enumerate(zip(canvases, pages), start=1):

    canvas_id = canvas.get("@id", "")
    match = re.search(r"-(\d+)/canvas$", canvas_id)

    canvas_number = int(match.group(1)) if match else None
    mets_order = page.get("ORDER")
    mets_page_id = page.get("ID")

    if canvas_number != position:
        issues.append(f"Position {position}: unexpected Canvas number")

    if mets_order != str(position):
        issues.append(f"Position {position}: unexpected METS ORDER")

    if mets_page_id != f"PHYS_{position:04d}":
        issues.append(f"Position {position}: unexpected METS Page ID")

print("\nCross-Format Sequence Check")
print("Positions compared:", min(len(canvases), len(pages)))
print("Issues found:", len(issues))

for issue in issues[:10]:
    print("Issue:", issue)

# Inspect file references for the first page

first_page = pages[0]
file_pointers = first_page.findall("mets:fptr", ns)

print("\nFirst METS Page - File References")

for pointer in file_pointers:
    file_id = pointer.get("FILEID")
    print("FILEID:", file_id)

    file_element = root.find(
        f".//mets:file[@ID='{file_id}']",
        ns
    )

    if file_element is not None:
        print("MIME type:", file_element.get("MIMETYPE"))

        file_location = file_element.find("mets:FLocat", ns)

        if file_location is not None:
            href = file_location.get(
                "{http://www.w3.org/1999/xlink}href"
            )
            print("File location:", href)

# Compare with the first IIIF image reference

first_canvas = canvases[0]
image_url = first_canvas["images"][0]["resource"]["@id"]

print("\nFirst IIIF Canvas - Image Reference")
print("Image URL:", image_url)


# Compare IIIF images with METS DEFAULT files

def extract_image_key(url):
    match = re.search(r"/dc/(?:PPN)?(\d+)-(\d+)/", url)

    if match is None:
        return None

    object_id = match.group(1)
    page_number = int(match.group(2))

    return object_id, page_number


files_by_id = {
    file.get("ID"): file
    for file in root.findall(".//mets:file", ns)
}

image_issues = []

for position, (canvas, page) in enumerate(zip(canvases, pages), start=1):

    iiif_url = canvas["images"][0]["resource"]["@id"]

    default_pointer = next(
        (
            pointer
            for pointer in page.findall("mets:fptr", ns)
            if (pointer.get("FILEID") or "").endswith("_DEFAULT")
        ),
        None
    )

    if default_pointer is None:
        image_issues.append(f"Page {position}: missing DEFAULT pointer")
        continue

    mets_file = files_by_id.get(default_pointer.get("FILEID"))

    if mets_file is None:
        image_issues.append(f"Page {position}: missing file definition")
        continue

    location = mets_file.find("mets:FLocat", ns)

    if location is None:
        image_issues.append(f"Page {position}: missing file location")
        continue

    mets_url = location.get("{http://www.w3.org/1999/xlink}href", "")

    iiif_key = extract_image_key(iiif_url)
    mets_key = extract_image_key(mets_url)

    if iiif_key is None or mets_key is None or iiif_key != mets_key:
        image_issues.append(f"Page {position}: image identifier mismatch")

print("\nIIIF / METS Image Identifier Check")
print("Page pairs examined:", min(len(canvases), len(pages)))
print("Issues found:", len(image_issues))

for issue in image_issues[:10]:
    print("Issue:", issue)


if issues or image_issues:
    sys.exit(1)

sys.exit(0)