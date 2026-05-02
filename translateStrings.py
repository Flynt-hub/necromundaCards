from pathlib import Path
import csv
from deep_translator import GoogleTranslator

INPUT_CSV = Path("cards_text.csv")
OUTPUT_CSV = Path("cards_text.csv")
ERROR_CSV = Path("translation_errors.csv")

translator = GoogleTranslator(source="en", target="fr")

fields_to_translate = [
    ("title_en", "title_fr"),
    ("type_en", "type_fr"),
    ("text_en", "text_fr"),
]

errors = []

def safe_translate(text, file, field):
    text = (text or "").strip()

    if not text:
        return ""

    try:
        result = translator.translate(text)
        return result if result else text

    except Exception as e:
        print()
        print("ERREUR TRADUCTION")
        print(f"Fichier : {file}")
        print(f"Champ   : {field}")
        print(f"Texte   : {text}")
        print(f"Erreur  : {type(e).__name__}: {e}")

        errors.append({
            "file": file,
            "field": field,
            "text": text,
            "error_type": type(e).__name__,
            "error": str(e),
        })

        # fallback : on garde l'anglais pour ne pas bloquer le pipeline
        return text

with INPUT_CSV.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for row in rows:
    file = row.get("file", "")

    for src_field, dst_field in fields_to_translate:
        row[dst_field] = safe_translate(
            row.get(src_field, ""),
            file,
            src_field,
        )

with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

with ERROR_CSV.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["file", "field", "text", "error_type", "error"],
    )
    writer.writeheader()
    writer.writerows(errors)

print()
print(f"Traduction générée : {OUTPUT_CSV}")
print(f"Erreurs enregistrées : {ERROR_CSV}")
print(f"Nombre d'erreurs : {len(errors)}")