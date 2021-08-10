import math
import PointChargeClass

def getFieldLocationsXDimension(margin, width, height,
        fieldType, direction, spaceIntoLinesDivider):
    numRows = (height - 2 * margin) // spaceIntoLinesDivider
    cellHeight = (height - 2 * margin) // numRows
    
    startingIndex = 0 if fieldType == 'E' else 1
    result = []
    for index in range(startingIndex, numRows, 2):
        y = margin + index * cellHeight
        result.append((0, y, width, y))
    return result

def getFieldLocationsYDimension(margin, width, height,
        fieldType, direction, spaceIntoLinesDivider):
    numCols = (width - 2 * margin) // spaceIntoLinesDivider
    cellWidth = (width - 2 * margin) // numCols
    index = 0 if fieldType == 'E' else 1
    result = []
    for num in range(0, numCols // 2 + 1):
        x = margin + index * cellWidth
        result.append((x, 0, x, height))
        index += 2
    return result

def getFieldLocationsZDimension(margin, width, height,
        fieldType, direction, spaceIntoLinesDivider):
    numRows = (height - 2 * margin) // spaceIntoLinesDivider
    numCols = (width - 2 * margin) // spaceIntoLinesDivider
    cellHeight = (height - 2 * margin) // numRows
    cellWidth = (width - 2 * margin) // numCols
    
    startingIndex = 0 if fieldType == 'E' else 1
    result = []
    for row in range(0, numRows):
        for index in range(startingIndex, numCols, 2):
            x0 = margin + index * cellWidth
            y0 = margin + row * cellHeight
            result.append((x0, y0, x0 + cellWidth, y0 + cellHeight))
        startingIndex = 0 if startingIndex == 1 else 1
    return result

def getFieldLocations(width, height, fieldType, direction):
    margin = 15
    spaceIntoLinesDivider = 40
    if direction == 'L' or direction == 'R':
        return getFieldLocationsXDimension(margin, width, height,
                fieldType, direction, spaceIntoLinesDivider)
    elif direction == 'U' or direction == 'D':
        return getFieldLocationsYDimension(margin, width, height,
                fieldType, direction, spaceIntoLinesDivider)
    elif direction == 'I' or direction == 'O':
        return getFieldLocationsZDimension(margin, width, height, 
                fieldType, direction, spaceIntoLinesDivider)

def cartesianToGraphicsX(cartX, width):
    return cartX + width // 2

def cartesianToGraphicsY(cartY, height):
    return -cartY + height // 2

def graphicsToCartesianX(graphicsX, width):
    return graphicsX - width // 2

def graphicsToCartesianY(graphicsY, height):
    return -(graphicsY - height // 2)

def calculateBearingAngleBetween(xEffected, yEffected, xCause, yCause):
    result = []
    if xEffected < xCause:
        result.append('R')
    elif xEffected > xCause:
        result.append('L')
    
    dx = abs(xEffected - xCause)
    dy = abs(yEffected - yCause)
    if dy == 0:
        return result
    elif dx == 0:
        if yEffected < yCause:
            result.append('D')
        elif yEffected > yCause:
            result.append('U')
        return result
    theta = math.degrees(math.atan(dy/dx))
    result.append(theta)

    if yEffected < yCause:
        result.append('D')
    elif yEffected > yCause:
        result.append('U')
    return result

def calculateOppositeBearingAngle(bearingIn):
    result = []
    result.append(PointChargeClass.PointCharge.getOppositeDirection(bearingIn[0]))
    if len(bearingIn) == 1:
        return result
    result.append(bearingIn[1])
    result.append(PointChargeClass.PointCharge.getOppositeDirection(bearingIn[2]))
    return result
