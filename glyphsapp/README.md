# Amiga Bitmap Font Tools for Glyphs.app

## Glyphs.app Scripts

- `openAmigaFont.py` opens an Amiga font descriptor file in Glyphs from the Scripts menu.
- `openAmigaJsonFont.py` opens .afontjson files in Glyphs from the Scripts menu.

## What's an .afontjson file?
It's a JSON representation of a font descriptor file. Usually created from the Node.js script in the `/node` folder

### Installation

Copy all the files in the `glyphsapp/scripts` folder into the Glyphs.app scripts folder. Restart Glyphs.

## Glyphs.app Plugins

`OpenAmigaJsonFont.glyphsFileFormat` opens .afontjson files in Glyphs from the Open... dialog. This is experimental at present - the plan is to attempt to open native fonts too at some stage. 

### Installation

Double click on the plugin. Restart Glyphs.