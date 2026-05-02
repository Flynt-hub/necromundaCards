#!/usr/bin/env bash
set -euo pipefail

INPUT_DIR="TacticsCards"
OUTPUT_DIR="TacticsSheets"

mkdir -p "$OUTPUT_DIR"

# A3 portrait à 300 DPI
PAGE_W=3508
PAGE_H=4961

# Carte Magic 63 x 88 mm à 300 DPI
CARD_W=744
CARD_H=1039

# Grille
COLS=3
ROWS=4
CARDS_PER_PAGE=$((COLS * ROWS))

# Pas d'espace entre les cartes
GAP=0

# Marges calculées automatiquement pour centrer la grille
GRID_W=$((COLS * CARD_W + (COLS - 1) * GAP))
GRID_H=$((ROWS * CARD_H + (ROWS - 1) * GAP))

START_X=$(((PAGE_W - GRID_W) / 2))
START_Y=$(((PAGE_H - GRID_H) / 2))

mapfile -d '' FILES < <(
    find "$INPUT_DIR" -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \) -print0 | sort -z
)
TOTAL=${#FILES[@]}
PAGE=0

for ((i = 0; i < TOTAL; i += CARDS_PER_PAGE)); do
    PAGE=$((PAGE + 1))
    OUT="$OUTPUT_DIR/sheet_$(printf "%03d" "$PAGE").png"

    echo "Création de $OUT"

    # Page A3 blanche forcée en PNG couleur RGBA
    magick \
        -size "${PAGE_W}x${PAGE_H}" \
        xc:white \
        -colorspace sRGB \
        -type TrueColorAlpha \
        "PNG32:$OUT"

    for ((j = 0; j < CARDS_PER_PAGE; j++)); do
        IDX=$((i + j))
        [[ $IDX -ge $TOTAL ]] && break

        FILE="${FILES[$IDX]}"

        COL=$((j % COLS))
        ROW=$((j / COLS))

        X=$((START_X + COL * (CARD_W + GAP)))
        Y=$((START_Y + ROW * (CARD_H + GAP)))

        # Important : mktemp puis ajout explicite de l'extension .png
        TMP="$(mktemp /tmp/card_XXXXXX).png"

        magick "$FILE" \
            -auto-orient \
            -colorspace sRGB \
            -type TrueColorAlpha \
            -resize "${CARD_W}x${CARD_H}^" \
            -gravity center \
            -extent "${CARD_W}x${CARD_H}" \
            "PNG32:$TMP"

        # Composite forcé en PNG couleur RGBA
        magick "$OUT" "$TMP" \
            -geometry "+${X}+${Y}" \
            -composite \
            "PNG32:$OUT"

        rm "$TMP"
    done
done
