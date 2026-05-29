from pathlib import Path
import csv
import textwrap
from PIL import Image, ImageDraw, ImageFont

INPUT_CSV = Path("cards_text.csv")
OUTPUT_DIR = Path("translated_cards")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

zones = {
    "title": (28, 28, 345, 53),
    "type": (28, 298, 300, 318),
    "text": (29, 330, 340, 480),
}

# May vary based on the available fonts. Adjust if needed.
TITLE_FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf", 18)
TYPE_FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf", 15)
TEXT_FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman.ttf", 13)

TEXT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (208, 200, 197)
TEXT_BACKGROUND_COLOR = (239, 237, 238)

def draw_wrapped_text(draw, text, box, font, line_spacing=3, padding_left=0, padding_top=0, paragraph_spacing=1):
    x1, y1, x2, y2 = box

    x1 += padding_left
    y1 += padding_top

    max_width = x2 - x1
    y = y1

    line_height = font.getbbox("Ag")[3] - font.getbbox("Ag")[1] + line_spacing

    paragraphs = text.split("\n")

    for para in paragraphs:
        words = para.split()
        line = ""
        lines = []

        for word in words:
            test = line + (" " if line else "") + word
            bbox = draw.textbbox((0, 0), test, font=font)

            if bbox[2] - bbox[0] <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = word

        if line:
            lines.append(line)

        # Dessin des lignes
        for line in lines:
            if y + line_height > y2:
                return
            draw.text((x1, y), line, font=font, fill=TEXT_COLOR)
            y += line_height

    y = y1

    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = line + (" " if line else "") + word
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word

    if line:
        lines.append(line)

    line_height = font.getbbox("Ag")[3] - font.getbbox("Ag")[1] + line_spacing

    for line in lines:
        if y + line_height > y2:
            break
        draw.text((x1, y), line, font=font, fill=TEXT_COLOR)
        y += line_height

def clear_box(draw, box, fill):
    draw.rectangle(box, fill=fill)

def sanitize_folder_name(name):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, "_")

    name = name.strip()

    if not name:
        name = "Unknown"

    return name

with INPUT_CSV.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f, delimiter=';')
    rows = list(reader)

for row in rows:
    img = Image.open(row["file"]).convert("RGB")
    draw = ImageDraw.Draw(img)
    # Effacer les anciennes zones
    clear_box(draw, zones["title"], BACKGROUND_COLOR)
    clear_box(draw, zones["type"], BACKGROUND_COLOR)
    clear_box(draw, zones["text"], TEXT_BACKGROUND_COLOR)
    # Réécrire en français
    draw.text((zones["title"][0], zones["title"][1]), row["title_fr"], font=TITLE_FONT, fill=TEXT_COLOR)
    draw.text((zones["type"][0], zones["type"][1]), row["type_fr"], font=TYPE_FONT, fill=TEXT_COLOR)

    draw_wrapped_text(
        draw,
        row["text_fr"],
        zones["text"],
        TEXT_FONT,
        line_spacing=3,
    )

    folder_name = sanitize_folder_name(row["type_fr"])

    card_output_dir = OUTPUT_DIR / folder_name
    card_output_dir.mkdir(parents=True, exist_ok=True)

    output = card_output_dir / f"{Path(row['file']).stem}_fr.png"

    img.save(output)

    print(f"Carte générée : {output}")