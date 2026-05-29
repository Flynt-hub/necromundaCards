# WHERE AM I ?

If you're a player of Warhammer 40,000: Necromunda, you'll find here all the tactical cards existing in the game (as of May 2026).
An unknown contributor recreated all existing cards using an online Magic: The Gathering card creator.

All these cards can be found in this repository under TacticsCards, or in the original repository: https://www.dropbox.com/scl/fo/fk0ekrk69ji1uhotjqe2v/ANI3e76aagG5ImU5jp_2Va8?rlkey=5m9k11kc7buzigi8hcd10zaqg&st=iy1flzbp&dl=0

# This repository

This repository contains small Bash/Python scripts to:

- extract text from the cards
- store it in a CSV file
- translate it
- recreate cards using the translations
- generate printable sheets and PDFs

# How to install ?

Make sure you can run shell scripts (native on macOS and Linux).

If you're on Windows, you will probably need to use WSL.

In PowerShell, type:

```powershell
wsl --install
```

Make sure you have python 3.14 installed on your machine.
You will also need to install the following dependencies.

## MacOS

```shell
brew install imagemagick
brew install tesseract
brew install tesseract-lang
brew install ghostscript
````

## Linux

```shell
sudo apt update

sudo apt install -y \
    imagemagick \
    tesseract-ocr \
    tesseract-ocr-eng \
    ghostscript
````
 ## Windows

Download and install python
    https://www.python.org/downloads/windows/
Do not forget to tick "Add Python to PATH"

Download Tesseract
    https://github.com/UB-Mannheim/tesseract/wiki
Then add the installation folder to your PATH.

Download and install Magick
    https://imagemagick.org/download/#windows&gsc.tab=0
While installing, tick "Install legacy utilities (e.g. convert)" and "Add application directory to your system path"

Download and install Ghostscript
    https://ghostscript.com/releases/gsdnld.html

As a personal recommendation, for less complexity, consider using a Docker container or a Linux virtual machine.

Anyway, Add the dependencies to the project using pip:
```shell
pip install -r requirements.txt
````

# How to use

Once everything is correctly installed, the hardest part is done.
You'll have to execute the first script from the root of the project
Edit the script beforehand to change the fieldnames, as they are currently configured for French.
```python
    python3.14 ./extractStringsFromAllCards.py
```

This will create a cards_text.csv containing all card text.

You may want to use automatic translation.
Before doing so, edit the translation script to change the target language, and update the field names you changed in the previous script
```python
    python3.14 ./translateStrings.py
```
BUT!
I tried automatic translation for French and the results were quite messy.
In the end, I translated all cards manually.
You may want to find a better translation workflow.

Then, once the translations are done
```python
    python3.14 ./createTranslatedCard.py
```

This will create a 'translated_cards' directory containing all translated cards.
Check carefully that everything looks correct (there are around 550 cards...).

Finally, to generate printable sheets:
```shell
    ./makeSheets.sh
```
This will create the TacticsSheets directory containing all printable sheets and a PDF ready for printing.

Congratulation, you have finish !

Now print the cards and enjoy losing friends while playing this wonderfully unbalanced game ^^

N.B: existing TacticsSheet directory contain french cards. So just print the PDF in it if you're french.