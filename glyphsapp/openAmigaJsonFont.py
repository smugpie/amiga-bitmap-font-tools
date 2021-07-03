#MenuTitle: Open Amiga JSON Font
# -*- coding: utf-8 -*-
__doc__="""
Converts Amiga Bitmap Font from JSON data.
"""

import json
from metrics import getHeight, getDepth
from drawing import drawPixel
from style import getHumanReadableStyle

Glyphs.clearLog()
print('Converting Amiga bitmap font...')

filePath = GetOpenFile('Choose a .afontjson file.', False)
binaryFile = open(filePath, encoding='utf-8')
amigaFont = json.load(binaryFile)
print('Parsing', amigaFont['name'])

glyphsFont = GSFont()
glyphsFont.familyName = amigaFont['name']
glyphsFont.upm = 1000
glyphsFont.descriptions['ENG'] = 'Converted by amiga-bitmap-font-tools'

Glyphs.fonts.append(glyphsFont)

glyphsFont.disableUpdateInterface()

try:
    master = glyphsFont.masters[0]
    print('Master:', master)
    master.name = getHumanReadableStyle(amigaFont['style'])

    fontSize = amigaFont['ySize']
    baseline = amigaFont['baseline']
    pixelSize = int(glyphsFont.upm / fontSize)
    print('Font:', glyphsFont) 
    print('Font size:', fontSize, '... Baseline:', baseline, '...Block size:', pixelSize)
    pixelsBelowBaseline = fontSize - baseline

    # work out x-height from the letter x (ASCII code 120)
    xHeight = getHeight(
        amigaFont['glyphs']['120']['bitmap'],
        pixelsBelowBaseline
    )
    if xHeight > 0:
        master.xHeight = xHeight * pixelSize

    # work out cap height from the letter E (ASCII code 69)
    capHeight = getHeight(
        amigaFont['glyphs']['69']['bitmap'],
        pixelsBelowBaseline
    )
    if capHeight > 0:
        master.capHeight = capHeight * pixelSize

    # work out ascender from the letter b (ASCII code 98)
    ascender = getHeight(
        amigaFont['glyphs']['98']['bitmap'],
        pixelsBelowBaseline
    )
    if ascender > 0:
        master.ascender = ascender * pixelSize

    # work out descender from the letter p (ASCII code 112)
    descender = getDepth(
        amigaFont['glyphs']['112']['bitmap'],
        pixelsBelowBaseline
    )
    if descender < 0:
        master.descender = descender * pixelSize

    for char, amigaGlyph in amigaFont['glyphs'].items():
        glyph = GSGlyph(amigaGlyph['character'])
        glyphsFont.glyphs.append(glyph)
        layer = glyph.layers[0]
        
        layer.width = ((amigaGlyph['spacing'] + amigaGlyph['kerning']) * pixelSize) if amigaFont['flags']['proportional'] else (amigaFont['xSize'] * pixelSize)

        for rowNumber, rowData in enumerate(amigaGlyph['bitmap']):
            rowPosition = fontSize - rowNumber - pixelsBelowBaseline
            for colNumber, colData in enumerate(rowData):
                colPosition = (colNumber + amigaGlyph['kerning']) if amigaFont['flags']['proportional'] else colNumber
                if colData == '1':
                    rect = drawPixel( rowPosition, colPosition, pixelSize )
                    layer.shapes.append(rect)
            layer.removeOverlap()

    print('Job done. Enjoy the pixels.')
except Exception as e:
    Glyphs.showMacroWindow()
    print('Script error!')
    import traceback
    print(traceback.format_exc())
    raise e
finally:
    glyphsFont.enableUpdateInterface()
