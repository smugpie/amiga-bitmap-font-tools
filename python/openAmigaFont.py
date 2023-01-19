#!/usr/bin/python3

import json
import sys
import getopt
from shutil import rmtree
from color import convertToColor
from metrics import getHeight, getDepth
from drawing import drawPixel
from style import getHumanReadableStyle, expandStyle, expandFlags
from utils import chunks, getRange, getNiceGlyphName, getCodeMap
from fontParts.world import *
from fontmake import font_project
from classes.FontStreamer import FontStreamer


def getBitmap(font, bitmapPointers, modulo, ySize):
    if (not isinstance(bitmapPointers, list)):
        return font.getBitArray(bitmapPointers, modulo, ySize)
    
    # Here we're attempting to sum all the values in the bit planes so
    # we'll end up with a colour index at each point in the bit array
    #  e.g. for 3 bitplanes we'll have an array of values from 0-7 at each
    # position
    bitplanes = [font.getBitArray(bitmapPointer, modulo, ySize) for bitmapPointer in bitmapPointers]
    bitmapRows = [([0] * modulo * 8) for _ in range(ySize)]

    for i, bitplane in enumerate(bitplanes):
        multiplier = 2 ** i
        for j in range(len(bitmapRows)):
            for k in range(len(bitmapRows[j])):
                bitmapRows[j][k] += int(bitplane[j][k]) * multiplier
    
    return bitmapRows


def addColorData(font):

    return font


def main(argv):
    inputFile = ''
    outputFile = ''
    fontFormat = ''
    codeMap = {}
    try:
        opts, args = getopt.getopt(argv,"hi:o:f:c:",["input_file=","output_file=","format=","codepage="])
    except getopt.GetoptError:
        print('Usage: openAmigaFont.py -i <inputfile> -o <outputfile> -f <format>')
        print('where format is one of ufo, ttf, otf')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: openAmigaFont.py -i <inputfile> -o <outputfile> -f <format>')
            print('where format is one of ufo, ttf, otf')
            sys.exit()
        elif opt in ("-i", "--input_file"):
            inputFile = arg
        elif opt in ("-o", "--output_file"):
            outputFile = arg
        elif opt in ("-f", "--format"):
            fontFormat = arg
            if fontFormat not in ('ufo', 'ttf', 'otf'):
                print('Format must be one of ufo, ttf, otf')
                sys.exit(2)
        elif opt in ("-c", "--codepage"):
            codeMap = getCodeMap(arg)

    if inputFile == '':
        print('Please specify the path to an input file')
        sys.exit(2)

    if inputFile.endswith('.font'):
        print('Please run the converter on a file inside the font folder')
        sys.exit(2)
    
    if outputFile == '':
        print('Please specify the path to an output file')
        sys.exit(2)
        
    if codeMap is None:
        print('Please specify a valid codepage')
        sys.exit(2)


    binaryFile = open(inputFile, 'rb')
    rawBytes = bytearray(binaryFile.read())

    # Create a class that can sequentially read the contents of the file
    # Font data starts at read position 78 
    font = FontStreamer(rawBytes, 78)

    # Font name is at position 26 though
    fontNameBytes = font.getBytesAt(26, 32)
    fontNameBytes[:] = fontNameBytes
    trimmedFontNameBytes = fontNameBytes.replace(b'\x00', b'')

    fontName = trimmedFontNameBytes.decode('ascii')
    ySize = font.readNextWord()
    style = expandStyle(font.readNextByte())
    flags = expandFlags(font.readNextByte())
    xSize = font.readNextWord()
    baseline = font.readNextWord()
    boldSmear = font.readNextWord()
    accessors = font.readNextWord()
    loChar = font.readNextByte()
    hiChar = font.readNextByte()
    fontDataPointer = font.readNextPointer()
    modulo = font.readNextWord()
    locationDataPointer = font.readNextPointer()

    locationData = font.getBytesAt(locationDataPointer)
    # there's an extra "notdef" character which is why we add 2
    charRange = hiChar - loChar + 2

    spacingDataPointer = font.readNextPointer()
    kerningDataPointer = font.readNextPointer()

    if flags['proportional']:
        kerningData = font.getBytesAt(kerningDataPointer)
        spacingData = font.getBytesAt(spacingDataPointer)

    if style['colorFont']:
        colorFlags = font.readNextWord()
        depth = font.readNextByte()
        predominantColor = font.readNextByte()
        lowestColor = font.readNextByte()
        highestColor = font.readNextByte()
        planePick = font.readNextByte()
        planeOnOff = font.readNextByte()
        colorDataPointer = font.readNextPointer()
        colorRawData = font.getBytesAt(colorDataPointer, 8)
        numberOfColors = int.from_bytes(colorRawData[2:4], byteorder='big', signed=True)
        colorTablePointer = int.from_bytes(colorRawData[4:8], byteorder='big', signed=True)

        colorTableRawData = font.getBytesAt(colorTablePointer, numberOfColors * 2)
        colors = []
        for colorIndex in range(2 ** depth):
            color = int.from_bytes(colorTableRawData[colorIndex * 2:colorIndex * 2 + 2], byteorder='big', signed=True)
            colors.append(convertToColor(color))

        colorBitplanePointers = []
        for i in range(depth):
            colorBitplanePointers.append(font.readNextPointer())

    bitmapRows = getBitmap(
        font,
        colorBitplanePointers if style["colorFont"] else fontDataPointer,
        modulo,
        ySize
    )

    print('Parsing', fontName)

    glyphs = {}

    for i in range(0, charRange):
        charCode = loChar + i
        defaultGlyphName = '.notdef' if charCode > hiChar else getNiceGlyphName(charCode)
        unicodeInt, glyphName = codeMap.get(charCode, (charCode, defaultGlyphName))
        locationStart = int.from_bytes(locationData[i * 4:i * 4 + 2], byteorder='big', signed=False)
        bitLength = int.from_bytes(locationData[i * 4 + 2:i * 4 + 4], byteorder='big', signed=False)
        charCodeIndex = '.notdef' if charCode > hiChar else str(unicodeInt)
        glyphs[charCodeIndex] = {
            "character": '.notdef' if charCode > hiChar else chr(unicodeInt),
            "glyphName": glyphName,
            "bitmap": list(map(lambda arr: getRange(arr, locationStart, bitLength), bitmapRows))
        }
        if flags['proportional']:
            glyphs[charCodeIndex]['kerning'] = int.from_bytes(kerningData[i * 2: i * 2 + 2], byteorder='big', signed=True)
            glyphs[charCodeIndex]['spacing'] = int.from_bytes(spacingData[i * 2: i * 2 + 2], byteorder='big', signed=True)


    outputFont = NewFont(familyName=fontName, showInterface=False)
    outputFont.info.unitsPerEm = 1000

    try:
        if style['colorFont']:
            outputFont.layers[0].color = colors[1]["fontColor"]
            outputFont.layers[0].name = f'{getHumanReadableStyle(style)}1'

            for i in range(2, numberOfColors):
                outputFont.newLayer(f'{getHumanReadableStyle(style)}{i}', colors[i]["fontColor"])

        else:
            outputFont.layers[0].name = getHumanReadableStyle(style)

        pixelSize = int(outputFont.info.unitsPerEm / ySize)
        print('Font size:', ySize, '... Width', xSize, '... Baseline:', baseline, '...Block size:', pixelSize)
        pixelsBelowBaseline = ySize - baseline

        # work out x-height from the letter x (ASCII code 120)
        xHeight = getHeight(glyphs['120']['bitmap'], pixelsBelowBaseline)
        if xHeight > 0:
            outputFont.info.xHeight = xHeight * pixelSize

        # work out cap height from the letter E (ASCII code 69)
        capHeight = getHeight(glyphs['69']['bitmap'], pixelsBelowBaseline)
        if capHeight > 0:
            outputFont.info.capHeight = capHeight * pixelSize

        # work out ascender from the letter b (ASCII code 98)
        ascender = getHeight(glyphs['98']['bitmap'], pixelsBelowBaseline)
        if ascender > 0:
            outputFont.info.ascender = ascender * pixelSize

        # work out descender from the letter p (ASCII code 112)
        descender = getDepth(glyphs['112']['bitmap'], pixelsBelowBaseline)
        if descender < 0:
            outputFont.info.descender = descender * pixelSize

        for char, amigaGlyph in glyphs.items():
            if amigaGlyph['character'] == '.notdef':
                glyphName = '.notdef'
            else:
                unicodeInt = ord(amigaGlyph['character'])
                glyphName = amigaGlyph['glyphName']
                print('Creating', unicodeInt, glyphName)     

            for i, layer in enumerate(outputFont.layers):
                glyph = layer.newGlyph(glyphName)
                if amigaGlyph['character'] != '.notdef':
                    glyph.unicode = unicodeInt

                glyph.width = ((amigaGlyph['spacing'] + amigaGlyph['kerning']) * pixelSize) if flags['proportional'] else (xSize * pixelSize)
                if glyph.width < 0:
                    glyph.width = 0

                for rowNumber, rowData in enumerate(amigaGlyph['bitmap']):
                    rowPosition = ySize - rowNumber - pixelsBelowBaseline
                    for colNumber, colData in enumerate(rowData):
                        colPosition = (colNumber + amigaGlyph['kerning']) if flags['proportional'] else colNumber
                        if int(colData) == i + 1:
                            rect = drawPixel( rowPosition, colPosition, pixelSize )
                            glyph.appendContour(rect)
                
                glyph.removeOverlap()

        if style['colorFont']:
            palette = [col["fontColor"] for col in colors]
            mapping = [[f"Color{idx}", idx] for idx in range(1, len(colors))]

            outputFont.lib["com.github.googlei18n.ufo2ft.colorPalettes"] = [palette]
            outputFont.lib["com.github.googlei18n.ufo2ft.colorLayerMapping"] = mapping


        if fontFormat == 'ufo':
            outputFont.save(outputFile)
        else:
            outputFont.save('./tmp/tmpFont.ufo')
            fontmaker = font_project.FontProject()
            ufo = fontmaker.open_ufo('./tmp/tmpFont.ufo')
            if fontFormat == 'otf':
                fontmaker.build_otfs([ufo], output_path=outputFile)
            else:
                fontmaker.build_ttfs([ufo], output_path=outputFile)
            rmtree('./tmp/tmpFont.ufo')

        print('Job done. Enjoy the pixels.')
    except Exception as e:
        print('Script error!')
        raise e

if __name__ == "__main__":
   main(sys.argv[1:])
