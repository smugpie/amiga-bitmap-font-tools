# Amiga Bitmap Font Tools

## Introduction

Some Glyphs.app scripts, written in Python, to open Amiga bitmap font files.

And a set of tools, written in Node.js, to query the contents of Amiga bitmap font files and export the data as JSON.

You can find some explanation of what's going on here at https://andrewgraham.dev.


## Glyphs.app Scripts

`openAmigaFont.py` opens an Amiga font descriptor file in Glyphs from the Scripts menu.

`openAmigaJsonFont.py` opens .afontjson files (see below) in Glyphs from the Scripts menu.

### Installation

Copy all the files in the `glyphsapp/scripts` folder into the Glyphs.app scripts folder. Restart Glyphs.

## Glyphs.app Plugins

`OpenAmigaJsonFont.glyphsFileFormat` opens .afontjson files (see below) in Glyphs from the Open... dialog.

### Installation

Double click on the plugin. Restart Glyphs.
## Node.js

Install node and/or nvm. The scripts are tested on Node.js v14.

### Installation

Open a terminal then

```
cd node
npm i
```

### Scripts

`readFontContents.js` reads the contents of `.font` files and extracts the data in JSON format. Change the file path in line 9 to choose the font you want to read. (I might change this to pass in the file path as an argument at some stage.)

```
node readFontContents.js > output.afontjson
```

`readFontDescriptor.js` reads the contents of font descriptor files (files with numeric filenames) and extracts the data in JSON format. Change the font name and size in lines 9 and 10 to choose the font you want to read.

```
node readFontDescriptor.js > output.afontjson
```


## Sample fonts

Webcleaner, a set of fonts designed for Amiga web browsers, are available in the `fonts` directory for your experimentation. Have fun!
