# Amiga Bitmap Font Tools for Node.js

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
