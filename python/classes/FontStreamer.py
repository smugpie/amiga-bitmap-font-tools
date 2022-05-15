# FontStreamer
# Takes a font file and streams bytes/words sequentially

from utils import chunks

class FontStreamer:
    def __init__(self, rawFontFile, readPosition):
        self.rawFontFile = rawFontFile
        # strip the first 32 bytes off to make the pointer locations accurate
        self.fontFile = rawFontFile[32:]
        self.readPosition = readPosition if readPosition else 0


    def setReadPosition(self, readPosition):
        self.readPosition = readPosition


    def readNextByte(self):
        byte = int.from_bytes(self.fontFile[self.readPosition:self.readPosition + 1], byteorder='big', signed=False)
        self.readPosition += 1
        return byte


    def readNextWord(self):
        word = int.from_bytes(self.fontFile[self.readPosition:self.readPosition + 2], byteorder='big', signed=False)
        self.readPosition += 2
        return word


    def readNextPointer(self):
        ptr = int.from_bytes(self.fontFile[self.readPosition:self.readPosition + 4], byteorder='big', signed=False)
        self.readPosition += 4
        return ptr


    def getBytesAt(self, start, length=None):
        if length:
            return self.fontFile[start:start + length]
        
        return self.fontFile[start:]

    def getBitArray(self, pointer, modulo, ySize):
        fontBitmapData = self.getBytesAt(pointer, modulo * ySize)
        # From https://stackoverflow.com/questions/43787031/python-byte-array-to-bit-array
        fontBitArray = ''.join(format(byte, '08b') for byte in fontBitmapData)
        chunkedArray = list(chunks(fontBitArray, modulo * 8))
        return [list(row) for row in chunkedArray]
