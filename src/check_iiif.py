
import json

with open("data/raw/PPN867445300_manifest.json", encoding="utf-8") as file:
    manifest = json.load(file)

canvases = manifest["sequences"][0]["canvases"]

missing_images = []

for canvas in canvases:
    images = canvas.get("images", [])

    if not images:
        missing_images.append(canvas.get("@id"))
        continue

    image_url = images[0].get("resource", {}).get("@id")

    if not image_url:
        missing_images.append(canvas.get("@id"))

print("Total canvases:", len(canvases))
print("Canvases without image URL:", len(missing_images))

for canvas_id in missing_images:
    print("Missing image URL:", canvas_id)



canvas_ids = []

for canvas in canvases:
    canvas_id = canvas.get("@id")

    if canvas_id:
        canvas_ids.append(canvas_id)

unique_ids = set(canvas_ids)

print("Canvases with ID:", len(canvas_ids))
print("Unique Canvas IDs:", len(unique_ids))
print("Missing Canvas IDs:", len(canvases) - len(canvas_ids))
print("Duplicate Canvas IDs:", len(canvas_ids) - len(unique_ids))



invalid_dimensions = []

for canvas in canvases:
    width = canvas.get("width")
    height = canvas.get("height")

    valid = (
        type(width) is int and width > 0
        and type(height) is int and height > 0
    )

    if not valid:
        invalid_dimensions.append(canvas.get("@id"))

print("Invalid dimensions:", len(invalid_dimensions))
