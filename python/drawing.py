from fontParts.world import dispatcher

# from https://github.com/mekkablue/Glyphs-Scripts/blob/master/Paths/Fill%20Up%20with%20Rectangles.py
def drawRect( myBottomLeft, myTopRight ):
    RContour = dispatcher['RContour']
    RPoint = dispatcher['RPoint']
    myRect = RContour()
    myCoordinates = [
        [ myBottomLeft[0], myBottomLeft[1] ],
        [ myTopRight[0], myBottomLeft[1] ],
        [ myTopRight[0], myTopRight[1] ],
        [ myBottomLeft[0], myTopRight[1] ]
    ]

    for thisPoint in myCoordinates:
        newPoint = RPoint()
        newPoint.type = 'line'
        newPoint.x = thisPoint[0]
        newPoint.y = thisPoint[1]
        myRect.appendPoint( point=newPoint )

    myRect.closed = True
    return myRect

def drawPixel( rowPosition, colPosition, hPixelSize, vPixelSize ):
    bottomLeft = (colPosition * hPixelSize, rowPosition * vPixelSize)
    topRight = ((colPosition + 1) * hPixelSize, (rowPosition + 1) * vPixelSize)
    return drawRect(bottomLeft, topRight)
