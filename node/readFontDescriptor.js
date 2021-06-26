// readFontDescriptor.js
// Converts an Amiga numeric font file and outputs details in JSON format

const fs = require('fs');
const path = require('path');
const BitArray = require('node-bitarray');
const _ = require('lodash');

const fontName = 'WebLight';
const fontSize = 32;

const rawFontFile = fs.readFileSync(
    path.join(__dirname, `../fonts/webcleaner/${fontName}/${fontSize}`)
);

// strip the first 32 bytes off to make the pointer locations accurate
const fontFile = rawFontFile.slice(32); 

const bitIsSet = (value, bit) => {
    return !!(value & (2 ** bit)); 
}

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
    disk: bitIsSet(flags, 1),
    proportional: bitIsSet(flags, 5),
    designed: bitIsSet(flags, 6)
});

const ySize = fontFile.readUInt16BE(78);
const style = fontFile.readUInt8(80);
const flags = fontFile.readUInt8(81);
const xSize = fontFile.readUInt16BE(82);
const baseline = fontFile.readUInt16BE(84);
const boldSmear = fontFile.readUInt16BE(86);
const accessors = fontFile.readUInt16BE(88);
const loChar = fontFile.readUInt8(90);
const hiChar = fontFile.readUInt8(91);

const charRange = hiChar - loChar + 2; // There's an extra "notdef" character

fontDataStart = fontFile.readUInt32BE(92);
const modulo = fontFile.readUInt16BE(96);
locationDataStart = fontFile.readUInt32BE(98);
spacingDataStart = fontFile.readUInt32BE(102);
kerningDataStart = fontFile.readUInt32BE(106);

const locationData = fontFile.slice(locationDataStart);
const kerningData = fontFile.slice(kerningDataStart);
const spacingData = fontFile.slice(spacingDataStart);

const fontBitmapData = fontFile.slice(fontDataStart, fontDataStart + (modulo * ySize));
const fontBitArray = BitArray.fromBuffer(fontBitmapData).toJSON();
const fontBitmapRows = _.chunk(fontBitArray, modulo * 8);

const fontData = {
    name: `${fontName}${fontSize}`,
    ySize,
    flags: expandFlags(flags),
    style: expandStyle(style),
    xSize,
    baseline,
    boldSmear,
    accessors,
    loChar,
    hiChar,
    fontDataStart,
    locationDataStart,
    spacingDataStart,
    kerningDataStart,
    modulo,
    glyphs: {}
};

for (let i = 0; i < charRange; i += 1) {
    const charCode = loChar + i;
    const locationStart = locationData.readUInt16BE(i * 4);
    const byteLength = locationData.readUInt16BE((i * 4) + 2);
    fontData.glyphs[charCode > hiChar ? 'notdef' : charCode] = {
        character: charCode > hiChar ? 'notdef' : String.fromCharCode(charCode),
        kerning: kerningData.readInt16BE(i * 2),
        spacing: spacingData.readInt16BE(i * 2),
        locationStart,
        byteLength,
        bitmap: fontBitmapRows.map((row) => row.slice(locationStart, locationStart + byteLength))
    }
};

console.log(JSON.stringify(fontData));

/* If you just want to output a single character, use this
fontData.glyphs[97].bitmap.forEach((row) => {
    console.log(row.join('').replace(/1/g, '##').replace(/0/g, '..'));
});
 */
