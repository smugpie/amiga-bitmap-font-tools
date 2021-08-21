from GlyphsApp import GSNode, GSLINE, GSPath

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

def drawPixel( rowPosition, colPosition, pixelSize ):
    bottomLeft = (colPosition * pixelSize, rowPosition * pixelSize)
    topRight = ((colPosition + 1) * pixelSize, (rowPosition + 1) * pixelSize)
    return drawRect(bottomLeft, topRight)
