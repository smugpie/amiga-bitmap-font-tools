// readFontDescriptor.js
// Converts an Amiga numeric font file and outputs details in JSON format
const fs = require('fs');
const path = require('path');

const _ = require('lodash');
const { expandStyle, expandFlags, expandColorFlags, getBitArray } = require('./helpers/utils');
const { convertToColor } = require('./helpers/color');
const FontStreamer = require('./classes/FontStreamer');

const [fontPath] = process.argv.slice(2);

if (!fontPath) {
    console.log('Please specify a font path')
    process.exit()
}

const rawFontFile = fs.readFileSync(
    path.join(__dirname, fontPath)
);

// Create a class that can sequentially read the contents of the file
// Font data starts at read position 78 
const font = new FontStreamer(rawFontFile, 78);

// Font name is at position 26 though
const fontName = font.getBytesAt(26, 32).toString().replace(/\u0000/g, '');

const ySize = font.readNextWord();
const style = expandStyle(font.readNextByte());
const flags = expandFlags(font.readNextByte());
const xSize = font.readNextWord();
const baseline = font.readNextWord();
const boldSmear = font.readNextWord();
const accessors = font.readNextWord();
const loChar = font.readNextByte();
const hiChar = font.readNextByte();
const fontDataPointer = font.readNextPointer();
const modulo = font.readNextWord();
const locationDataPointer = font.readNextPointer();


let fontData = {
    name: fontName,
    ySize,
    style,
    flags,
    xSize,
    baseline,
    boldSmear,
    accessors,
    loChar,
    hiChar,
    fontDataPointer,
    modulo,
    locationDataPointer,
    glyphs: {}
};

const locationData = font.getBytesAt(locationDataPointer);
const charRange = hiChar - loChar + 2; // There's an extra "notdef" character

const spacingDataPointer = font.readNextPointer();
const kerningDataPointer = font.readNextPointer();
let spacingData;
let kerningData;


if (flags.proportional) {
    kerningData = font.getBytesAt(kerningDataPointer);
    spacingData = font.getBytesAt(spacingDataPointer);

    fontData = {
        ...fontData,
        spacingDataPointer,
        kerningDataPointer
    }
}

let colorBitplanePointers;

if (style.colorFont) {
    const colorFlags = font.readNextWord();
    const depth = font.readNextByte();
    const predominantColor = font.readNextByte();
    const lowestColor = font.readNextByte();
    const highestColor = font.readNextByte();
    const planePick = font.readNextByte();
    const planeOnOff = font.readNextByte();
    const colorDataPointer = font.readNextPointer();
    const colorRawData = font.getBytesAt(colorDataPointer, 8);
    const numberOfColors = colorRawData.readUInt16BE(2);
    const colorTablePointer = colorRawData.readUInt32BE(4);

    const colorTableRawData = font.getBytesAt(colorTablePointer, numberOfColors * 2);
    colors = [];
    for (let colorIndex = 0; colorIndex < 2 ** depth; colorIndex += 1) {
        const color = colorTableRawData.readUInt16BE(colorIndex * 2);
        colors.push(convertToColor(color));
    }

    colorBitplanePointers = [];
    for (let i = 0; i < depth; i += 1) {
        colorBitplanePointers.push(font.readNextPointer());
    }

    fontData = {
        ...fontData,
        colorFlags: expandColorFlags(colorFlags),
        depth,
        predominantColor,
        lowestColor,
        highestColor,
        planePick,
        planeOnOff,
        colorData: {
            numberOfColors,
            colors,
            colorBitplanePointers
        }
    }
}

let bitmapRows;
if (style.colorFont) {
    // Here we're attempting to sum all the values in the bit planes so
    // we'll end up with a colour index at each point in the bit array
    // e.g. for 3 bitplanes we'll have an array of values from 0-7 at each
    // position
    const bitplanes = colorBitplanePointers.map(bitplanePointer => {
        return font.getBitArray(bitplanePointer, modulo, ySize);
    })

    bitmapRows = [];
    for (let i = 0; i < ySize; i += 1) {
        bitmapRows.push(new Array(modulo * 8).fill(0));
    }

    for (let i = 0; i < fontData.depth; i += 1) {
        const bitplane = bitplanes[i];
        const multiplier = 2 ** i;
        for (let j = 0; j < bitmapRows.length; j += 1) {
            for (let k = 0; k < bitmapRows[j].length; k += 1) {
                bitmapRows[j][k] += bitplane[j][k] * multiplier;
            }
        }
    }

} else {
    bitmapRows = font.getBitArray(fontDataPointer, modulo, ySize);
}

for (let i = 0; i < charRange; i += 1) {
    const charCode = loChar + i;

    const locationStart = locationData.readUInt16BE(i * 4);
    const bitLength = locationData.readUInt16BE((i * 4) + 2);
    const index = charCode > hiChar ? 'notdef' : charCode;
    fontData.glyphs[index] = {
        character: charCode > hiChar ? '.notdef' : String.fromCharCode(charCode),
        locationStart,
        bitLength,
        bitmap: bitmapRows.map((row) => row.slice(locationStart, locationStart + bitLength).join(''))
    }

    if (flags.proportional) {
        fontData.glyphs[index] = {
            kerning: kerningData.readInt16BE(i * 2),
            spacing: spacingData.readInt16BE(i * 2),
            ...fontData.glyphs[index]
        };
    }
};

console.log(JSON.stringify(fontData));

// If you just want to output a single character, use this
// fontData.glyphs[65].bitmap.forEach((row) => {
//     console.log(row.replace(/0/g, '.'));
// });

