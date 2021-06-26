#MenuTitle: Convert Amiga Bitmap Font
# -*- coding: utf-8 -*-
__doc__="""
Converts Amiga Bitmap Font Data into a Glyphs font.
"""

import json

# work out the height of a glyph in order to calculate dimensions
# like ascender, capHeight etc
def getHeight(glyphBitmap, fontSize, pixelsBelowBaseline):
    height = fontSize
    for row in glyphBitmap:
        if sum(row) > 0:
            break
        height -= 1

    return height - pixelsBelowBaseline + 1

# work out the depth of a glyph in order to calculate descender
def getDepth(glyphBitmap, pixelsBelowBaseline):
    reversedGlyphBitmap = list(reversed(glyphBitmap))
    height = 0
    for row in reversedGlyphBitmap:
        if sum(row) > 0:
            break
        height += 1

    return height - pixelsBelowBaseline + 1

# from https://github.com/mekkablue/Glyphs-Scripts/blob/master/Paths/Fill%20Up%20with%20Rectangles.py
def drawRect( myBottomLeft, myTopRight ):
    myRect = GSPath()
    myCoordinates = [
        [ myBottomLeft[0], myBottomLeft[1] ],
        [ myTopRight[0], myBottomLeft[1] ],
        [ myTopRight[0], myTopRight[1] ],
        [ myBottomLeft[0], myTopRight[1] ]
    ]

    for thisPoint in myCoordinates:
        newNode = GSNode()
        newNode.type = GSLINE
        newNode.position = ( thisPoint[0], thisPoint[1] )
        myRect.nodes.append( newNode )

    myRect.closed = True
    return myRect

# gets a name from Amiga font style flags
def getHumanReadableStyle( style ):
    if style['normal']:
        return 'Regular'
    name = []
    if style['bold']:
        name.append('Bold')
    if style['italic']:
        name.append('Italic')
    if style['extended']:
        name.append('Extended')
    separator = ' '
    return separator.join(name)


Glyphs.clearLog()
print('Converting Amiga bitmap font...')

file = open(
    'weblight32.afontjson',
    encoding='utf-8'
)
amigaFont = json.load(file)
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
    unitBlock = int(glyphsFont.upm / fontSize)
    print('Font:', glyphsFont) 
    print('Font size:', fontSize, '... Baseline:', baseline, '...Block size:', unitBlock)
    pixelsBelowBaseline = fontSize - baseline

    # work out x-height from the letter x (ASCII code 120)
    xHeight = getHeight(
        amigaFont['glyphs']['120']['bitmap'],
        fontSize,
        pixelsBelowBaseline
    )
    if xHeight > 0:
        master.xHeight = xHeight * unitBlock

    # work out cap height from the letter E (ASCII code 69)
    capHeight = getHeight(
        amigaFont['glyphs']['69']['bitmap'],
        fontSize,
        pixelsBelowBaseline
    )
    if capHeight > 0:
        master.capHeight = capHeight * unitBlock

    # work out ascender from the letter b (ASCII code 98)
    ascender = getHeight(
        amigaFont['glyphs']['98']['bitmap'],
        fontSize,
        pixelsBelowBaseline
    )
    if ascender > 0:
        master.ascender = ascender * unitBlock

    # work out descender from the letter p (ASCII code 112)
    descender = getDepth(
        amigaFont['glyphs']['112']['bitmap'],
        pixelsBelowBaseline
    )
    if descender < 0:
        master.descender = descender * unitBlock

    for char, amigaGlyph in amigaFont['glyphs'].items():
        glyph = GSGlyph(amigaGlyph['character'])
        glyphsFont.glyphs.append(glyph)
        layer = glyph.layers[0]
        layer.width = (amigaGlyph['spacing'] + amigaGlyph['kerning']) * unitBlock

        for rowNumber, rowData in enumerate(amigaGlyph['bitmap']):
            rowPosition = fontSize - rowNumber - pixelsBelowBaseline
            for colNumber, colData in enumerate(rowData):
                colPosition = colNumber + amigaGlyph['kerning']
                if colData == 1:
                    bottomLeft = (colPosition * unitBlock, rowPosition * unitBlock)
                    topRight = ((colPosition + 1) * unitBlock, (rowPosition + 1) * unitBlock)
                    rect = drawRect(bottomLeft, topRight)
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
