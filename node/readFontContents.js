// readFontContents.js
// Reads the Amiga .font file and outputs details

const fs = require('fs');
const path = require('path');

const MAXFONTPATH = 256;
const FONTENTRYSIZE = MAXFONTPATH + 4;
const fontFile = fs.readFileSync(path.join(__dirname, '../fonts/webcleaner/WebBold.font'));

const bitIsSet = (value, bit) => {
    return !!(value & (2 ** bit)); 
}

const getFileContentsType = (fontFile) => {
    const fileContentsType = fontFile.readUInt16BE(0);
    const fileContentsFormats = {
        0xF00: 'FontContents',
        0xF02: 'TFontContents',
        0xF03: 'Scalable'
    }

    return fileContentsFormats[fileContentsType] || 'Unknown';
}

const getNumberOfEntries = (fontFile) => fontFile.readUInt16BE(2);

const expandStyle = (style) => ({
    value: style,
    normal: style === 0,
    underlined: bitIsSet(style, 0),
    bold: bitIsSet(style, 1),
    italic: bitIsSet(style, 2),
    extended: bitIsSet(style, 3),
    colorfont: bitIsSet(style, 6),
    tagged: bitIsSet(style, 7)
});

const expandFlags = (flags) => ({
    value: flags,
    rom: bitIsSet(flags, 0),
    disk: bitIsSet(flags, 1),
    reversed: bitIsSet(flags, 2),
    tallDot: bitIsSet(flags, 3),
    wideDot: bitIsSet(flags, 4),
    proportional: bitIsSet(flags, 5),
    designed: bitIsSet(flags, 6),
    removed: bitIsSet(flags, 7)
});

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
        flags: expandFlags(flags),
        style: expandStyle(style)
    };
}

console.log((fontData.entries));
