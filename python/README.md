# Amiga Bitmap Font Tools: Python scripts

## What's here

A script to convert a native Amiga font descriptor file to a font usable by PC/Macs.

Uses [fontParts](https://fontparts.robotools.dev/en/stable/) and [fontmake](https://github.com/googlefonts/fontmake).

## Prerequisites

- Python - tested on v3.11.
## Installation

The best way of running Python is to create a virtual environment. Open a terminal in this folder (`/python`)

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

```
python ./openAmigaFont.py [OPTIONS] <input_file> <output_file>
```

Where
- `input_file` should be a Amiga font descriptor file - e.g. `../fonts/native/Magnet/32`
- `output_file` should be the name of your output file - e.g. `Magnet32.otf`

and the options are:
- `-f`, `--format` which can be any one of `ufo`, `ttf` or `otf` (default `ttf`)
- `-t`, `--tmp_path` is the location for temporary files
- `-c`, `--code_page` is the code page, only `AmigaPL` codepage is implemented
- `-a`, `--aspect_ratio` can be used to control the aspect ratio of the pixels - handy if you want to stretch or narrow each glyph. For a half-width font, use 0.5 (default `1.0`)
- `-p`, `--pixel_component` constructs the font out of a pixel component. Handy if you want to change the shape of the pixel - why not try dots for a dot matrix effect!

## Sample fonts

There are a few fonts of my own making in `../fonts` so feel free to try the script out on those!

The scripts work on colour fonts too. You can find examples of Amiga colour fonts on Aminet. Particularly
recommended is [The Kara Collection on Aminet](https://aminet.net/package/text/bfont/TKC_ColorFonts).
