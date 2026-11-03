import sys
import xml.etree.ElementTree as ET

default_path = "data/raw/PPN867445300_mets.xml"

xml_path = sys.argv[1] if len(sys.argv) > 1 else default_path

root = ET.parse(xml_path).getroot()
ns = {"mets": "http://www.loc.gov/METS/"}

# Collect all descriptive metadata IDs
dmd_sections = root.findall("mets:dmdSec", ns)

metadata_ids = set()

for section in dmd_sections:
    section_id = section.get("ID")
    if section_id:
        metadata_ids.add(section_id)

# Collect references from the logical structure
logical = root.find("mets:structMap[@TYPE='LOGICAL']", ns)

referenced_ids = set()

for div in logical.findall(".//mets:div", ns):
    dmdid = div.get("DMDID")

    if dmdid:
        for reference in dmdid.split():
            referenced_ids.add(reference)

# Compare both sets
missing_references = referenced_ids - metadata_ids
unused_metadata = metadata_ids - referenced_ids

print("Metadata sections:", len(dmd_sections))
print("Unique metadata IDs:", len(metadata_ids))
print("Unique referenced IDs:", len(referenced_ids))
print("References without metadata:", len(missing_references))
print("Unreferenced metadata sections:", len(unused_metadata))

for item in sorted(missing_references):
    print("Broken reference:", item)

for item in sorted(unused_metadata):
    print("Unreferenced metadata:", item)


# Validate structural links

physical = root.find("mets:structMap[@TYPE='PHYSICAL']", ns)

logical_ids = {
    div.get("ID")
    for div in logical.findall(".//mets:div", ns)
    if div.get("ID")
}

physical_ids = {
    div.get("ID")
    for div in physical.findall(".//mets:div", ns)
    if div.get("ID")
}

links = root.findall("mets:structLink/mets:smLink", ns)

xlink = "{http://www.w3.org/1999/xlink}"

broken_links = []

for link in links:
    source = link.get(xlink + "from")
    target = link.get(xlink + "to")

    if source not in logical_ids or target not in physical_ids:
        broken_links.append((source, target))

print("\nStructural Link Validation")
print("Total structural links:", len(links))
print("Broken structural links:", len(broken_links))

for source, target in broken_links:
    print("Invalid link:", source, "->", target)
