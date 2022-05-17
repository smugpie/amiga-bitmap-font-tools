# Amiga Bitmap Font Tools: Python scripts

## What's here

A script to convert a native Amiga font descriptor file to a font usable by PC/Macs.

Uses [fontParts](https://fontparts.robotools.dev/en/stable/) and [fontmake](https://github.com/googlefonts/fontmake).

## Prerequisites

- Python - tested on v3.9.
## Installation

The best way of running Python is to create a virtual environment. Open a terminal in this folder (`/python`)

```
python3 -m venv .
source ./bin/activate
pip3 install fontparts fontmake
```

## Usage

```
python ./openAmigaFont.py -i <input_file> -o <output_file> -f <font_format>
```

Where
- `-i` should be a Amiga font descriptor file - e.g. `../fonts/native/Magnet/32`
- `-o` should be the name of your output file - e.g. `Magnet32.otf`
- `-f` can be any one of `ufo`, `ttf` or `otf`

## Sample fonts

There are a few fonts of my own making in `../fonts` so feel free to try the script out on those!

The scripts work on colour fonts too. You can find examples of Amiga colour fonts on Aminet. Particularly
recommended is [The Kara Collection on Aminet](https://aminet.net/package/text/bfont/TKC_ColorFonts).
