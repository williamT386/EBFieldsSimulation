import PointChargeClass, EFieldClass, BFieldClass, Calculations
import math
from cmu_112_graphics import *

# Sets the app constants
def setConstants(app):
    app.pointChargeRadius = 10
    app.displayMenuRectWidth = 200
    app.displayMenuRectHeight = 150
    app.menuExitDimensions = 20
    app.maxPointCharges = 3
    app.defaultWidth = app.width
    app.defaultHeight = app.height
    app.userOptionsWidth = app.height // 4
    app.optionsCX = app.width - app.userOptionsWidth // 2
    app.optionsDrawingWidth = int(app.userOptionsWidth * 0.8)
    app.optionsSurroundingRectWidth = app.optionsDrawingWidth // 2

    app.pointChargeOptionYs = (120, 180)
    app.eFieldsOptionYs = (200, 260)
    app.bFieldsOptionYs = (280, 340)
    app.interactionsBetweenPCOptionYs = (360, 420)
    app.resetButtonOptionYs = (440, 470)
    app.showPCInteractions = False
    app.checkboxCX = app.optionsCX - app.optionsDrawingWidth // 3
    app.optionArrowLength = 30
    app.optionShortLineArrowLength = 15
    app.arrowThickness = 2
    app.pcColor = 'Black'
    app.eArrowColor = 'Dark Blue'
    app.bArrowColor = 'Dark Red'
    
    app.askCX = (app.width - app.optionsDrawingWidth) // 2
    app.askCY = app.height // 2
    app.askWidth = 500
    app.askHeight = 250
    app.askSubmitXs = (app.askCX + 30, app.askCX + 120)
    app.askSubmitYs = (app.askCY + 10, app.askCY + 50)
    app.inOutSymbolMargin = 10

def appStarted(app):
    setConstants(app)
    reset(app)

def reset(app):
    app.allPointCharges = []
    app.allEFields = []
    app.allBFields = []
    app.displayMenu = None
    app.displayMenuRectCX = None
    app.displayMenuRectCY = None
    app.errorMessage = None
    app.errorMessageTimer = None

    app.draggingPCOption = False
    app.draggingEFieldOption = False
    app.draggingBFieldOption = False
    app.draggingPC = None
    app.draggingEField = None
    app.draggingBField = None
    app.isAskDataForEField = False
    app.isAskDataForBField = False

    app.askDataFieldDirection = None

# Returns distance between 2 points
def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# Sets data for the display menu
def setDisplayMenuInfo(app):
    rectWidth = app.displayMenuRectWidth
    rectHeight = app.displayMenuRectHeight
    margin = 10
    radius = app.pointChargeRadius

    app.displayMenuRectCX = app.displayMenu.cx
    if app.displayMenuRectCX + rectWidth / 2 >= app.width:
        app.displayMenuRectCX = app.displayMenu.cx - rectWidth / 2 - margin
    elif app.displayMenuRectCX - rectWidth / 2 < 0:
        app.displayMenuRectCX = app.displayMenu.cx + rectWidth / 2 - margin
    
    app.displayMenuRectCY = app.displayMenu.cy - rectHeight // 2 - margin - radius
    if app.displayMenuRectCY - rectHeight // 2 < 0:
        app.displayMenuRectCY = app.displayMenu.cy + rectHeight // 2 + margin + radius

# Returns the location to set the menu
def getMenuLocations(app):
    cx = app.displayMenuRectCX
    cy = app.displayMenuRectCY
    width = app.displayMenuRectWidth
    height = app.displayMenuRectHeight
    return cx, cy, width, height

# Check if clicked outside the menu
def checkClickedOutOfMenu(app, event):
    if app.displayMenu != None:
        menuCX, menuCY, menuWidth, menuHeight = getMenuLocations(app)
        if not (menuCX - menuWidth // 2 <= event.x <= menuCX + menuWidth // 2 and 
                menuCY - menuHeight // 2 <= event.y <= menuCY + menuHeight // 2):
            app.displayMenu = None

# Check if clicked the exit of the menu
def checkClickedMenuExit(app, event):
    if app.displayMenu != None:
        menuCX, menuCY, menuWidth, menuHeight = getMenuLocations(app)
        exitDimensions = app.menuExitDimensions
        if (menuCX + menuWidth // 2 - exitDimensions <= event.x <= menuCX + menuWidth // 2 and 
                menuCY - menuHeight // 2 <= event.y <= menuCY - menuHeight // 2 + exitDimensions):
            app.displayMenu = None
            return True
    return False

def checkClickedAskExit(app, event):
    exitDimensions = app.menuExitDimensions
    if (app.askCX + app.askWidth // 2 - exitDimensions <= event.x <=
            app.askCX + app.askWidth // 2 and
            app.askCY - app.askHeight // 2 <= event.y <=
            app.askCY - app.askHeight // 2 + exitDimensions):
        app.isAskDataForEField = False
        app.isAskDataForBField = False

def isValidDirectionEntry(app, key):
    key = key.upper()
    return (key == 'U' or key == 'D' or key == 'L' or key == 'R' or 
            key == 'I' or key == 'O')

def keyPressed(app, event):
    if app.isAskDataForEField or app.isAskDataForBField:
        if isValidDirectionEntry(app, event.key):
            app.askDataFieldDirection = event.key
        else:
            setErrorMessage(app, 'Please enter a valid direction.')
            app.askDataFieldDirection = None

# Removes the error message after 3000 ms
def timerFired(app):
    if app.errorMessageTimer != None:
        app.errorMessageTimer += app.timerDelay
        if app.errorMessageTimer >= 3000:
            app.errorMessage = None
            app.errorMessageTimer = None

def clickedInOptionPane(app, event):
    if (app.optionsCX - app.optionsSurroundingRectWidth <= event.x <= 
            app.optionsCX + app.optionsSurroundingRectWidth and 
            app.resetButtonOptionYs[0] <= event.y <= app.resetButtonOptionYs[1]):
        reset(app)
    elif(app.optionsCX - app.optionsDrawingWidth <= event.x <= 
            app.optionsCX + app.optionsDrawingWidth):
        # point charge option
        if(app.pointChargeOptionYs[0] <= event.y <= 
                app.pointChargeOptionYs[1]):
            app.draggingPCOption = True
        # electric field option
        elif(app.eFieldsOptionYs[0] <= event.y <= 
                app.eFieldsOptionYs[1]):
            app.draggingEFieldOption = True
        # magnetic field option
        elif(app.bFieldsOptionYs[0] <= event.y <= 
                app.bFieldsOptionYs[1]):
            app.draggingBFieldOption = True
        # interactions option
        elif(app.interactionsBetweenPCOptionYs[0] <= event.y <= 
                app.interactionsBetweenPCOptionYs[1]):
            app.showPCInteractions = not app.showPCInteractions

def hasDuplicateFieldInList(app, currentField, fieldList):
    for field in fieldList:
        if currentField == field:
            return True
    return False

def checkClickedSubmit(app, event):
    if (app.askSubmitXs[0] <= event.x <= app.askSubmitXs[1] and
            app.askSubmitYs[0] <= event.y <= app.askSubmitYs[1]):
        if app.isAskDataForEField:
            app.isAskDataForEField = False
            currentEField = EFieldClass.EField(app.askDataFieldDirection)
            if not hasDuplicateFieldInList(app, currentEField, app.allEFields):
                app.allEFields.append(currentEField)
        else:
            app.isAskDataForBField = False
            currentBField = BFieldClass.BField(app.askDataFieldDirection)
            if not hasDuplicateFieldInList(app, currentBField, app.allBFields):
                app.allBFields.append(currentBField)
        app.askDataFieldDirection = None
        #app.allEFields

def mousePressed(app, event):
    checkClickedOutOfMenu(app, event)
    if checkClickedMenuExit(app, event):
        return

    # clicked in option pane
    if event.x + app.pointChargeRadius >= app.width - app.userOptionsWidth:
        clickedInOptionPane(app, event)
        return

    if app.isAskDataForEField or app.isAskDataForBField:
        checkClickedAskExit(app, event)
        checkClickedSubmit(app, event)
        return

    # check if clicked inside a point charge
    for currentPC in app.allPointCharges:
        if (currentPC.cx - app.pointChargeRadius <= event.x <= 
                currentPC.cx + app.pointChargeRadius and
                (currentPC.cy - app.pointChargeRadius <= event.y <= 
                currentPC.cy + app.pointChargeRadius)):
            app.displayMenu = currentPC
            setDisplayMenuInfo(app)
            return

def mouseDragged(app, event):
    if app.isAskDataForEField or app.isAskDataForBField:
        return

    if app.draggingPCOption:
        app.draggingPC = (event.x, event.y)
    elif app.draggingEFieldOption:
        app.draggingEField = (event.x, event.y)
    elif app.draggingBFieldOption:
        app.draggingBField = (event.x, event.y)

def addPC(app, event):
    # released in option pane
    if (event.x + app.pointChargeRadius >= app.width - app.userOptionsWidth or 
            event.x - app.pointChargeRadius <= 0 or 
            event.y - app.pointChargeRadius <= 0 or
            event.y + app.pointChargeRadius >= app.height):
        app.draggingPCOption = False
        app.draggingPC = None
        return

    # check if new location would cause overlap
    for currentPC in app.allPointCharges:
        if (distance(event.x, event.y, currentPC.cx, currentPC.cy) <= 
                2*app.pointChargeRadius):
            app.draggingPCOption = False
            app.draggingPC = None
            return

    # check if too many point charges
    if len(app.allPointCharges) == app.maxPointCharges:
        setErrorMessage(app, f"Can only have up to {app.maxPointCharges} " + 
                            "point charges on the screen")
        app.draggingPCOption = False
        app.draggingPC = None
        return
    newPointCharge = PointChargeClass.PointCharge(event.x, event.y)
    app.allPointCharges.append(newPointCharge)
    app.draggingPCOption = False
    app.draggingPC = None

# TODO: create cancel effect when U and D fields are created of same field type
def mouseReleased(app, event):
    if app.draggingPC != None:
        addPC(app, event)
    elif app.draggingEField != None:
        app.isAskDataForEField = True
        app.draggingEFieldOption = False
        app.draggingEField = None
    elif app.draggingBField != None:
        app.isAskDataForBField = True
        app.draggingBFieldOption = False
        app.draggingBField = None

# Sets an error message to a given message and starts the error message timer
def setErrorMessage(app, message):
    app.errorMessage = message
    app.errorMessageTimer = 0

# Draws everything
def redrawAll(app, canvas):
    drawCompass(app, canvas)
    drawUserOptions(app, canvas)
    drawFields(app, canvas, 'E')
    drawFields(app, canvas, 'B')
    drawPointCharges(app, canvas)
    drawMenu(app, canvas)
    drawErrorMessage(app, canvas)
    drawDraggingObject(app, canvas)
    if app.isAskDataForEField:
        drawAskDataForField(app, canvas, 'Electric')
    elif app.isAskDataForBField:
        drawAskDataForField(app, canvas, 'Magnetic')

# Draws a compass arrow
def drawCompassArrow(app, canvas, arrowLength, allArrowsCX, allArrowsCY, 
        direction, textIn):
    (dx, dy) = direction
    endX = allArrowsCX + dx * arrowLength
    endY = allArrowsCY + dy * arrowLength
    canvas.create_line(allArrowsCX, allArrowsCY, endX, endY)
    
    textMargin = 10
    if dy != 0:
        canvas.create_text(allArrowsCX, endY + textMargin * dy, 
                text = textIn, font = 'Arial 20', anchor = 'center')
    else:
        canvas.create_text(endX + textMargin * dx, allArrowsCY,
                text = textIn, font = 'Arial 20', anchor = 'center')

# Draws the compass
def drawCompass(app, canvas):
    canvas.create_rectangle(app.width - app.userOptionsWidth, app.height, 
            app.width, app.height - app.userOptionsWidth)
    allArrowsCX = app.width - app.userOptionsWidth // 2
    allArrowsCY = app.height - app.userOptionsWidth // 2
    arrowLength = app.userOptionsWidth // 2 - 25
    drawCompassArrow(app, canvas, arrowLength, allArrowsCX, allArrowsCY, 
            (0, -1), 'U')
    drawCompassArrow(app, canvas, arrowLength, allArrowsCX, allArrowsCY, 
            (0, 1), 'D')
    drawCompassArrow(app, canvas, arrowLength, allArrowsCX, allArrowsCY, 
            (-1, 0), 'L')
    drawCompassArrow(app, canvas, arrowLength, allArrowsCX, allArrowsCY, 
            (1, 0), 'R')

# Draws the options
def drawUserOptions(app, canvas):
    canvas.create_line(app.width - app.userOptionsWidth,
            0, app.width - app.userOptionsWidth, app.height - app.userOptionsWidth)
    
    canvas.create_text(app.optionsCX, 25, text = 'EBFields', 
            font = 'Arial 25 bold', anchor = 'center')
    canvas.create_text(app.optionsCX, 55, text = 'Simulation', 
            font = 'Arial 25 bold', anchor = 'center')
    
    canvas.create_text(app.optionsCX, 85, text = 'By William Tang',
            font = 'Arial 20', anchor = 'center')
    
    lineY = (85 + 10 + app.pointChargeOptionYs[0]) // 2
    canvas.create_line(app.width - app.userOptionsWidth,
            lineY, app.width, lineY)

    drawPointChargeOption(app, canvas)
    drawEFieldOption(app, canvas)
    drawBFieldOption(app, canvas)
    drawInteractionsBetweenPCOption(app, canvas)
    drawResetButton(app, canvas)

# Draws the point charge option
def drawPointChargeOption(app, canvas):
    canvas.create_rectangle(app.optionsCX - app.optionsDrawingWidth // 2,
            app.pointChargeOptionYs[0], 
            app.optionsCX + app.optionsDrawingWidth // 2,
            app.pointChargeOptionYs[1])
    checkBoxCY = ((app.pointChargeOptionYs[0] + 
            app.pointChargeOptionYs[1])//2)
    canvas.create_oval(app.checkboxCX - app.pointChargeRadius,
            checkBoxCY - app.pointChargeRadius,
            app.checkboxCX + app.pointChargeRadius,
            checkBoxCY + app.pointChargeRadius,
            fill = app.pcColor)
    canvas.create_text(app.checkboxCX + app.pointChargeRadius + 53, checkBoxCY, 
            text = 'Point Charge', font = 'Arial 15', anchor = 'center')

def drawEFieldOption(app, canvas):
    canvas.create_rectangle(app.optionsCX - app.optionsDrawingWidth // 2,
            app.eFieldsOptionYs[0], 
            app.optionsCX + app.optionsDrawingWidth // 2, 
            app.eFieldsOptionYs[1])
    checkBoxCY = ((app.eFieldsOptionYs[0] + 
            app.eFieldsOptionYs[1])//2)
    x0 = app.checkboxCX - app.pointChargeRadius - 5
    x1 = x0 + app.optionArrowLength
    canvas.create_line(x0, checkBoxCY, x1, checkBoxCY, 
            fill = app.eArrowColor, width = app.arrowThickness)
    angle = math.pi/4
    canvas.create_line(x1, checkBoxCY, 
            x1 - app.optionShortLineArrowLength * math.sin(angle),
            checkBoxCY - app.optionShortLineArrowLength * math.cos(angle),
            fill = app.eArrowColor, width = app.arrowThickness)
    canvas.create_line(x1, checkBoxCY, 
            x1 - app.optionShortLineArrowLength * math.sin(angle),
            checkBoxCY + app.optionShortLineArrowLength * math.cos(angle),
            fill = app.eArrowColor, width = app.arrowThickness)
    canvas.create_text(app.checkboxCX + 69, checkBoxCY, 
            text = 'Electric Field', font = 'Arial 15', anchor = 'center')

def drawBFieldOption(app, canvas):
    canvas.create_rectangle(app.optionsCX - app.optionsDrawingWidth // 2,
            app.bFieldsOptionYs[0], 
            app.optionsCX + app.optionsDrawingWidth // 2,
            app.bFieldsOptionYs[1])
    checkBoxCY = ((app.bFieldsOptionYs[0] + 
            app.bFieldsOptionYs[1])//2)
    x0 = app.checkboxCX - app.pointChargeRadius - 5
    x1 = x0 + app.optionArrowLength
    canvas.create_line(x0, checkBoxCY, x1, checkBoxCY, 
            fill = app.bArrowColor, width = app.arrowThickness)
    angle = math.pi/4
    canvas.create_line(x1, checkBoxCY, 
            x1 - app.optionShortLineArrowLength * math.sin(angle),
            checkBoxCY - app.optionShortLineArrowLength * math.cos(angle),
            fill = app.bArrowColor, width = app.arrowThickness)
    canvas.create_line(x1, checkBoxCY, 
            x1 - app.optionShortLineArrowLength * math.sin(angle),
            checkBoxCY + app.optionShortLineArrowLength * math.cos(angle),
            fill = app.bArrowColor, width = app.arrowThickness)
    canvas.create_text(app.checkboxCX + 67, checkBoxCY, 
            text = 'Magnetic Field', font = 'Arial 15', anchor = 'center')

def drawInteractionsBetweenPCOption(app, canvas):
    canvas.create_rectangle(app.optionsCX - app.optionsDrawingWidth // 2,
            app.interactionsBetweenPCOptionYs[0], 
            app.optionsCX + app.optionsDrawingWidth // 2, 
            app.interactionsBetweenPCOptionYs[1])
    
    # app.showPCInteractions
    checkBoxCY = ((app.interactionsBetweenPCOptionYs[0] + 
            app.interactionsBetweenPCOptionYs[1])//2)
    checkBoxDimensions = 10
    checkBoxColor = 'Green' if app.showPCInteractions else 'Red'
    canvas.create_rectangle(app.checkboxCX - checkBoxDimensions, 
            checkBoxCY - checkBoxDimensions, 
            app.checkboxCX + checkBoxDimensions,
            checkBoxCY + checkBoxDimensions, fill = checkBoxColor)
    textCX = ((app.checkboxCX + checkBoxDimensions // 2 + 
                app.optionsCX + app.optionsDrawingWidth // 2)//2 + 5)
    canvas.create_text(textCX, app.interactionsBetweenPCOptionYs[0] + 15, 
            text = 'Include electric', anchor = 'center')
    canvas.create_text(textCX, app.interactionsBetweenPCOptionYs[0] + 30, 
            text = 'fields by point', anchor = 'center')
    canvas.create_text(textCX, app.interactionsBetweenPCOptionYs[0] + 45, 
            text = 'charges', anchor = 'center')

def drawResetButton(app, canvas):
    canvas.create_rectangle(app.optionsCX - app.optionsSurroundingRectWidth // 2,
            app.resetButtonOptionYs[0], 
            app.optionsCX + app.optionsSurroundingRectWidth // 2,
            app.resetButtonOptionYs[1], width = 3)
    cy = (app.resetButtonOptionYs[0] + app.resetButtonOptionYs[1]) // 2
    canvas.create_text(app.optionsCX, cy, text = 'Reset', 
            font = 'Arial 20', anchor = 'center')

# Draws the menu if possible
def drawMenu(app, canvas):
    if app.displayMenu != None:
        width = app.displayMenuRectWidth
        height = app.displayMenuRectHeight
        canvas.create_rectangle(app.displayMenuRectCX - width // 2,
                app.displayMenuRectCY - height // 2,
                app.displayMenuRectCX + width // 2,
                app.displayMenuRectCY + height // 2,
                fill = 'blue')
        
        # Draw exit 
        exitDimensions = app.menuExitDimensions
        menuCX, menuCY, menuWidth, menuHeight = getMenuLocations(app)
        canvas.create_rectangle(menuCX + menuWidth // 2 - exitDimensions,
                menuCY - menuHeight // 2,
                app.displayMenuRectCX + width // 2,
                menuCY - menuHeight // 2 + exitDimensions,
                fill = 'red')
        
        # Draw exit cross
        crossMargin = 5
        canvas.create_line(menuCX + menuWidth // 2 - exitDimensions + crossMargin,
                menuCY - menuHeight // 2 + crossMargin,
                app.displayMenuRectCX + width // 2 - crossMargin,
                menuCY - menuHeight // 2 + exitDimensions - crossMargin, 
                fill = 'white', width = 2)
        canvas.create_line(menuCX + menuWidth // 2 - crossMargin,
                menuCY - menuHeight // 2 + crossMargin,
                menuCX + menuWidth // 2 - exitDimensions + crossMargin,
                menuCY - menuHeight // 2 + exitDimensions - crossMargin, 
                fill = 'white', width = 2)

# Draws the error message if possible
def drawErrorMessage(app, canvas):
    if app.errorMessage != None:
        textAndRectCX = app.width // 2
        textAndRectCY = app.height - 100
        textAndRectWidth = 400
        textAndRectHeight = 30
        canvas.create_rectangle(textAndRectCX - textAndRectWidth // 2, 
                textAndRectCY - textAndRectHeight // 2,
                textAndRectCX + textAndRectWidth // 2,
                textAndRectCY + textAndRectHeight // 2,
                fill = 'pink')
        canvas.create_text(textAndRectCX, textAndRectCY, text = app.errorMessage,
                anchor = 'center')

# Draws the point charges if possible
def drawPointCharges(app, canvas):
    for currentPointCharge in app.allPointCharges:
        canvas.create_oval(currentPointCharge.cx - app.pointChargeRadius,
                currentPointCharge.cy - app.pointChargeRadius,
                currentPointCharge.cx + app.pointChargeRadius,
                currentPointCharge.cy + app.pointChargeRadius,
                fill = app.pcColor)
        canvas.create_text(currentPointCharge.cx, currentPointCharge.cy,
                text = currentPointCharge.charge, fill = 'white')

def drawFieldItem(app, canvas, x0, y0, x1, y1, direction, color):
    angle = math.pi / 4
    errorShift = 2
    if direction == 'I':
        crossMargin = 8
        canvas.create_line(x0 + crossMargin, y0 + crossMargin, 
                x1 - crossMargin, y1 - crossMargin, fill = 'white')
        canvas.create_line(x0 + crossMargin, y1 - crossMargin, 
                x1 - crossMargin, y0 + crossMargin, fill = 'white')
    elif direction == 'O':
        cx = (x0 + x1) // 2
        cy = (y0 + y1) // 2
        canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, fill = 'white')
    elif direction == 'R':
        x0Arrow = x1 - app.optionShortLineArrowLength * math.cos(angle)
        yAArrow = y1 - app.optionShortLineArrowLength * math.sin(angle)
        yBArrow = y1 + app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(x0Arrow, yAArrow, x1, y1, x0Arrow, yBArrow, 
                fill = color)
    elif direction == 'L':
        x0 += errorShift
        x1Arrow = x0 + app.optionShortLineArrowLength * math.cos(angle)
        yAArrow = y1 - app.optionShortLineArrowLength * math.sin(angle)
        yBArrow = y1 + app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(x1Arrow, yAArrow, x0, y0, x1Arrow, yBArrow, 
                fill = color)
    elif direction == 'U':
        y0 += errorShift
        xAArrow = x0 - app.optionShortLineArrowLength * math.cos(angle)
        xBArrow = x0 + app.optionShortLineArrowLength * math.cos(angle)
        y1Arrow = y0 + app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(xAArrow, y1Arrow, x0, y0, xBArrow, y1Arrow, 
                fill = color)
    elif direction == 'D':
        y1 -= errorShift
        xAArrow = x1 - app.optionShortLineArrowLength * math.cos(angle)
        xBArrow = x1 + app.optionShortLineArrowLength * math.cos(angle)
        y1Arrow = y1 - app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(xAArrow, y1Arrow, x1, y1, xBArrow, y1Arrow, 
                fill = color)

def drawFields(app, canvas, fieldType):
    width = app.width - app.userOptionsWidth
    fieldList = app.allEFields if fieldType == 'E' else app.allBFields
    color = app.eArrowColor if fieldType == 'E' else app.bArrowColor
    for currentField in fieldList:
        currentListOfLocations = Calculations.getFieldLocations(
                width, app.height, fieldType, currentField.direction)
        for (x0, y0, x1, y1) in currentListOfLocations:
            if currentField.direction == 'I' or currentField.direction == 'O':
                canvas.create_oval(x0 + app.inOutSymbolMargin, 
                        y0 + app.inOutSymbolMargin, 
                        x1 - app.inOutSymbolMargin, 
                        y1 - app.inOutSymbolMargin, fill = color)
                drawFieldItem(app, canvas, x0 + app.inOutSymbolMargin, 
                        y0 + app.inOutSymbolMargin, 
                        x1 - app.inOutSymbolMargin, 
                        y1 - app.inOutSymbolMargin, currentField.direction, 
                        None)
            else:
                canvas.create_line(x0, y0, x1, y1, fill = color,
                        width = app.arrowThickness)
                drawFieldItem(app, canvas, x0, y0, x1, y1, 
                        currentField.direction, color)

def drawDraggingObject(app, canvas):
    if app.draggingPC != None:
        cx, cy = app.draggingPC
        canvas.create_oval(cx - app.pointChargeRadius,
            cy - app.pointChargeRadius, 
            cx + app.pointChargeRadius,
            cy + app.pointChargeRadius, fill = app.pcColor)
        canvas.create_text(cx, cy,
                text = '+', fill = 'white')
    elif app.draggingEField != None:
        x0 = app.draggingEField[0] - app.optionArrowLength // 2
        x1 = x0 + app.optionArrowLength
        checkBoxCY = app.draggingEField[1]
        canvas.create_line(x0, checkBoxCY, x1, checkBoxCY, 
            fill = app.eArrowColor, width = app.arrowThickness)
        angle = math.pi/4
        canvas.create_line(x1, checkBoxCY, 
                x1 - app.optionShortLineArrowLength * math.sin(angle),
                checkBoxCY - app.optionShortLineArrowLength * math.cos(angle),
                fill = app.eArrowColor, width = app.arrowThickness)
        canvas.create_line(x1, checkBoxCY, 
                x1 - app.optionShortLineArrowLength * math.sin(angle),
                checkBoxCY + app.optionShortLineArrowLength * math.cos(angle),
                fill = app.eArrowColor, width = app.arrowThickness)
    elif app.draggingBField != None:
        x0 = app.draggingBField[0] - app.optionArrowLength // 2
        x1 = x0 + app.optionArrowLength
        checkBoxCY = app.draggingBField[1]
        canvas.create_line(x0, checkBoxCY, x1, checkBoxCY, 
            fill = app.bArrowColor, width = app.arrowThickness)
        angle = math.pi/4
        canvas.create_line(x1, checkBoxCY, 
                x1 - app.optionShortLineArrowLength * math.sin(angle),
                checkBoxCY - app.optionShortLineArrowLength * math.cos(angle),
                fill = app.bArrowColor, width = app.arrowThickness)
        canvas.create_line(x1, checkBoxCY, 
                x1 - app.optionShortLineArrowLength * math.sin(angle),
                checkBoxCY + app.optionShortLineArrowLength * math.cos(angle),
                fill = app.bArrowColor, width = app.arrowThickness)

def drawAskDataForField(app, canvas, fieldType):
    canvas.create_rectangle(app.askCX - app.askWidth // 2,
            app.askCY - app.askHeight // 2,
            app.askCX + app.askWidth // 2,
            app.askCY + app.askHeight // 2,
            fill = 'Blue')
    
    # Draw exit 
    exitDimensions = app.menuExitDimensions
    canvas.create_rectangle(app.askCX + app.askWidth // 2 - exitDimensions,
            app.askCY - app.askHeight // 2,
            app.askCX + app.askWidth // 2,
            app.askCY - app.askHeight // 2 + exitDimensions,
            fill = 'red')
    
    # Draw exit cross
    crossMargin = 5
    canvas.create_line(app.askCX + app.askWidth // 2 - exitDimensions + crossMargin,
            app.askCY - app.askHeight // 2 + crossMargin,
            app.askCX + app.askWidth // 2 - crossMargin,
            app.askCY - app.askHeight // 2 + exitDimensions - crossMargin, 
            fill = 'white', width = 2)
    canvas.create_line(app.askCX + app.askWidth // 2 - crossMargin,
            app.askCY - app.askHeight // 2 + crossMargin,
            app.askCX + app.askWidth // 2 - exitDimensions + crossMargin,
            app.askCY - app.askHeight // 2 + exitDimensions - crossMargin, 
            fill = 'white', width = 2)
    
    # draw input textbox
    canvas.create_text(app.askCX , app.askCY - 70, text = 'Type Direction ' + 
            f'for new {fieldType} Field\n(U, D, L, R, I (in), O (out)):', 
            anchor = 'center', font = 'Arial 25', fill = 'white')
    canvas.create_rectangle(app.askCX - 170, app.askCY + 50,
            app.askCX, app.askCY + 10, fill = 'white')
    canvas.create_line(app.askCX - 10, app.askCY + 40, 
            app.askCX - 10, app.askCY + 20, width = 2)
    if app.askDataFieldDirection != None:
        canvas.create_text(app.askCX - 18, app.askCY + 30, 
                text = app.askDataFieldDirection.upper(), 
                font = 'Arial 18', anchor = 'center')
    
    # draw submit button
    canvas.create_rectangle(app.askCX + 30, app.askCY + 10,
            app.askCX + 120, app.askCY + 50, fill = 'white', width = 3)
    canvas.create_text(app.askCX + 75, app.askCY + 30, text = 'Submit', 
            font = 'Arial 20', anchor = 'center')

runApp(width = 1000, height = 700)