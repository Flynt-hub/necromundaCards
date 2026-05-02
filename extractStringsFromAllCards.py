from pathlib import Path
import csv
from PIL import Image, ImageOps, ImageFilter
import pytesseract

INPUT_DIR = Path("../TacticsCards")
OUTPUT_CSV = Path("cards_text.csv")

zones = {
    "title": (26, 28, 345, 53),
    "type": (26, 298, 300, 320),
    "text": (26, 330, 345, 480),
}

def preprocess(zone: Image.Image) -> Image.Image:
    zone = zone.convert("L")
    zone = ImageOps.autocontrast(zone)
    zone = zone.resize((zone.width * 3, zone.height * 3))
    zone = zone.filter(ImageFilter.SHARPEN)
    return zone

def ocr(zone: Image.Image) -> str:
    config = "--psm 6"
    text = pytesseract.image_to_string(zone, lang="eng", config=config)
    # return " ".join(text.split())
    return text.strip()

rows = []

for card_file in sorted(INPUT_DIR.rglob("*.png")):
    print(f"OCR: {card_file}")

    img = Image.open(card_file).convert("RGB")

    row = {
        "file": str(card_file),
        "title_en": "",
        "type_en": "",
        "text_en": "",
        "title_fr": "",
        "type_fr": "",
        "text_fr": "",
    }

    for name, box in zones.items():
        crop = img.crop(box)
        processed = preprocess(crop)
        row[f"{name}_en"] = ocr(processed)

    rows.append(row)

with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "file",
            "title_en",
            "type_en",
            "text_en",
            "title_fr",
            "type_fr",
            "text_fr",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

print()
print(f"OCR terminé : {len(rows)} cartes traitées")
print(f"CSV généré : {OUTPUT_CSV}")