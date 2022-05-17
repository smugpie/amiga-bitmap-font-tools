// readFontContents.js
// Reads the Amiga .font file and outputs details

const fs = require('fs');
const path = require('path');
const { expandStyle, expandFlags, getFileContentsType } = require('./helpers/utils');

const [fontPath] = process.argv.slice(2);

if (!fontPath) {
    console.log('Please specify a font path')
    process.exit()
}

const MAXFONTPATH = 256;
const FONTENTRYSIZE = MAXFONTPATH + 4;
const fontFile = fs.readFileSync(path.join(__dirname, fontPath));


const getNumberOfEntries = (fontFile) => fontFile.readUInt16BE(2);

const fontData = {
    fontContentsFormat: getFileContentsType(fontFile),
    numberOfEntries: getNumberOfEntries(fontFile),
    entries: {}
};

for (let offset = 4; offset < fontFile.byteLength; offset += FONTENTRYSIZE) {
    const fontEntry = fontFile.slice(offset, offset + FONTENTRYSIZE);
    const fontNameAndPointSize = fontEntry.slice(0, MAXFONTPATH);
    const [fontName, pointSize] = fontNameAndPointSize.toString('utf-8').replace(/\0/g, '').split('/');
    const ySize = fontEntry.readUInt16BE(MAXFONTPATH);
    const style = fontEntry.readUInt8(MAXFONTPATH + 2);
    const flags = fontEntry.readUInt8(MAXFONTPATH + 3);
    fontData.entries[pointSize] = {
        fontName,
        pointSize,
        ySize,
        flags: expandFlags(flags, true),
        style: expandStyle(style)
    };
}

console.log(JSON.stringify(fontData, null, 2));
