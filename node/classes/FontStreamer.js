// FontStreamer
// Takes a font file and streams bytes/words sequentially
const _ = require('lodash');
const BitArray = require('node-bitarray');

class FontStreamer {
    constructor(rawFontFile, readPosition) {
        this.rawFontFile = rawFontFile;
        // strip the first 32 bytes off to make the pointer locations accurate
        this.fontFile = rawFontFile.slice(32);
        // font data starts at position 78
        this.readPosition = readPosition || 0;
    }

    setReadPosition(readPosition) {
        this.readPosition = readPosition;
    }

    readNextByte() {
        const byte = this.fontFile.readUInt8(this.readPosition);
        this.readPosition += 1;
        return byte;
    }

    readNextWord() {
        const word = this.fontFile.readUInt16BE(this.readPosition);
        this.readPosition += 2;
        return word;
    }

    readNextPointer() {
        const ptr = this.fontFile.readUInt32BE(this.readPosition);
        this.readPosition += 4;
        return ptr;
    }

    getBytesAt(start, length) {
        return this.fontFile.slice(start, length ? start + length : undefined);
    }

    getBitArray = (pointer, modulo, ySize) => {
        const fontBitmapData = this.getBytesAt(pointer, modulo * ySize);
        const fontBitArray = BitArray.fromBuffer(fontBitmapData).toJSON();
        return  _.chunk(fontBitArray, modulo * 8);
    }
    
}

module.exports = FontStreamer
