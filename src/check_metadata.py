
import csv

with open("data/sample_metadata.csv", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    seen_ids = set()

    for record in reader:

        if record["title"].strip() == "":
            print("Missing title:", record["record_id"])

        if record["record_id"] in seen_ids:
            print("Duplicate ID:", record["record_id"])

        seen_ids.add(record["record_id"])
