from pathlib import Path
import csv
from PIL import Image, ImageOps, ImageFilter
import pytesseract

CARD_FILE = Path("Mined!.png")
OUTPUT_CSV = Path("mined_text.csv")

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
    return " ".join(text.split())

img = Image.open(CARD_FILE).convert("RGB")

row = {
    "file": str(CARD_FILE),
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
    writer.writerow(row)

print("OCR terminé.")
print(f"CSV généré : {OUTPUT_CSV}")
print(f"Images debug : {DEBUG_DIR}")

print()
print("Résultat OCR :")
print("Titre :", row["title_en"])
print("Type  :", row["type_en"])
print("Texte :", row["text_en"])