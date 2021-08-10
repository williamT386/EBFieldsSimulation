from cmu_112_graphics import *
import math
import PointChargeClass, EFieldClass, BFieldClass, Calculations

def drawAll(app, canvas):
    drawCompass(app, canvas)
    drawUserOptions(app, canvas)
    drawFields(app, canvas, 'E')
    drawFields(app, canvas, 'B')

    drawOriginDot(app, canvas)
    drawErrorMessage(app, canvas)
    drawDraggingObject(app, canvas)
    
    drawPCInteractions(app, canvas)
    drawFieldForces(app, canvas)
    drawPointCharges(app, canvas)
    drawMenu(app, canvas)
    if app.isAskDataForEField:
        drawAskDataForField(app, canvas, 'Electric')
    elif app.isAskDataForBField:
        drawAskDataForField(app, canvas, 'Magnetic')
    

# Returns the location to set the menu
def getMenuLocations(app):
    cx = app.displayMenuRectCX
    cy = app.displayMenuRectCY
    width = app.displayMenuRectWidth
    height = app.displayMenuRectHeight
    return cx, cy, width, height

# Draws a compass arrow
def drawCompassArrow(app, canvas, compassArrowLength, allArrowsCX, allArrowsCY, 
        direction, textIn):
    (dx, dy) = direction
    endX = allArrowsCX + dx * compassArrowLength
    endY = allArrowsCY + dy * compassArrowLength
    canvas.create_line(allArrowsCX, allArrowsCY, endX, endY)
    textMargin = 10
    if dy != 0:
        canvas.create_text(allArrowsCX, endY + textMargin * dy, 
                text = textIn, font = 'Arial 20', anchor = 'center')
    else:
        canvas.create_text(endX + textMargin * dx, allArrowsCY,
                text = textIn, font = 'Arial 20', anchor = 'center')
    
    angle = math.pi / 4
    errorShift = 2
    # direction is L
    if dx > 0:
        x0Arrow = endX - app.optionShortLineArrowLength * math.cos(angle)
        yAArrow = endY - app.optionShortLineArrowLength * math.sin(angle)
        yBArrow = endY + app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(x0Arrow, yAArrow, endX, endY, x0Arrow, yBArrow, 
                width = 1)
    # direction is R
    elif dx < 0:
        x1Arrow = endX + app.optionShortLineArrowLength * math.cos(angle)
        yAArrow = endY - app.optionShortLineArrowLength * math.sin(angle)
        yBArrow = endY + app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(x1Arrow, yAArrow, endX, endY, x1Arrow, yBArrow, 
                width = 1)
    # direction is U
    elif dy < 0:
        xAArrow = endX - app.optionShortLineArrowLength * math.cos(angle)
        xBArrow = endX + app.optionShortLineArrowLength * math.cos(angle)
        y1Arrow = endY + app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(xAArrow, y1Arrow, endX, endY, xBArrow, y1Arrow, 
                width = 1)
    # direction is D
    else:
        xAArrow = endX - app.optionShortLineArrowLength * math.cos(angle)
        xBArrow = endX + app.optionShortLineArrowLength * math.cos(angle)
        y1Arrow = endY - app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(xAArrow, y1Arrow, endX, endY, xBArrow, y1Arrow, 
                width = 1)

# Draws the compass
def drawCompass(app, canvas):
    canvas.create_rectangle(app.width - app.userOptionsWidth, app.height, 
            app.width, app.height - app.userOptionsWidth)
    allArrowsCX = app.width - app.userOptionsWidth // 2
    allArrowsCY = app.height - app.userOptionsWidth // 2
    compassArrowLength = app.userOptionsWidth // 2 - 25
    drawCompassArrow(app, canvas, compassArrowLength, allArrowsCX, allArrowsCY, 
            (0, -1), 'U')
    drawCompassArrow(app, canvas, compassArrowLength, allArrowsCX, allArrowsCY, 
            (0, 1), 'D')
    drawCompassArrow(app, canvas, compassArrowLength, allArrowsCX, allArrowsCY, 
            (-1, 0), 'L')
    drawCompassArrow(app, canvas, compassArrowLength, allArrowsCX, allArrowsCY, 
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
    drawCheckboxInteractions(app, canvas)
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
    x1 = x0 + app.compassArrowLength
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
    x1 = x0 + app.compassArrowLength
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

def drawCheckboxInteractions(app, canvas):
    canvas.create_rectangle(app.optionsCX - app.optionsDrawingWidth // 2,
            app.interactionsBetweenPCOptionYs[0], 
            app.optionsCX + app.optionsDrawingWidth // 2, 
            app.interactionsBetweenPCOptionYs[1])
    
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

def drawMenuBoard(app, canvas):
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

# Draws the menu if possible
def drawMenu(app, canvas):
    if app.displayMenu == None:
        return
    width = app.displayMenuRectWidth
    height = app.displayMenuRectHeight
    drawMenuBoard(app, canvas)
    
    titleCX = app.displayMenuRectCX - width // 2 + 15
    drawMenuDisplayInformation(app, canvas, width, height, titleCX)
    textboxCX = titleCX + 60

    drawXMenu(app, canvas, width, height, titleCX, textboxCX,
            app.submitButtonWidth, app.submitButtonHeight, app.submitButtonCX)
    
    drawYMenu(app, canvas, width, height, titleCX, textboxCX,
            app.submitButtonWidth, app.submitButtonHeight, app.submitButtonCX)

    drawChargeMenu(app, canvas, width, height, titleCX, textboxCX,
            app.submitButtonWidth, app.submitButtonHeight, app.submitButtonCX)
    
    drawVelocityDirectionMenu(app, canvas, width, height, titleCX, textboxCX,
            app.submitButtonWidth, app.submitButtonHeight, app.submitButtonCX)

    # Draw delete button
    canvas.create_rectangle(app.deleteButtonLocation[0],
            app.deleteButtonLocation[1],
            app.deleteButtonLocation[2],
            app.deleteButtonLocation[3],
            fill = 'white', width = 3)
    canvas.create_text(app.displayMenuRectCX, app.deleteButtonCY, 
            text = 'Delete', font = 'Arial 18', anchor = 'center')

def drawMenuDisplayInformation(app, canvas, width, height, titleCX):
    graphicsX = Calculations.graphicsToCartesianX(app.menuPointCharge.cx, 
            app.width - app.userOptionsWidth)
    graphicsY = Calculations.graphicsToCartesianY(app.menuPointCharge.cy, 
            app.height)
    canvas.create_text(titleCX, app.checkboxXLocation[1] - 75,
            text = f'Position: ({graphicsX}, {graphicsY})', fill = 'white', 
            font = 'Arial 17', anchor = 'w')
    canvas.create_text(titleCX, app.checkboxXLocation[1] - 52, 
            text = f'Charge: {app.menuPointCharge.charge}', fill = 'white', 
            font = 'Arial 17', anchor = 'w')
    canvas.create_text(titleCX, app.checkboxXLocation[1] - 29, 
            text = f'Velocity Direction: {app.menuPointCharge.velocityDirection}', 
            fill = 'white', font = 'Arial 17', anchor = 'w')

def drawXMenu(app, canvas, width, height, titleCX, textboxCX,
            submitButtonWidth, submitButtonHeight, submitButtonCX):
    canvas.create_text(titleCX, app.checkboxXLocation[1] - 10, 
            text = 'x: ', fill = 'white', 
            font = 'Arial 17', anchor = 'w')
    canvas.create_rectangle(app.checkboxXLocation[0],
            app.checkboxXLocation[1],
            app.checkboxXLocation[2],
            app.checkboxXLocation[3], fill = 'white')
    if app.menuSelected == 'x':
        canvas.create_line(app.checkboxXLocation[2] - 10,
                app.checkboxXLocation[1] + 5,
                app.checkboxXLocation[2] - 10,
                app.checkboxXLocation[3] - 5, width = 2)
    if app.menuPCX != None:
        canvas.create_text(app.checkboxXLocation[2] - 12, 
                (app.checkboxXLocation[1] + 5 + app.checkboxXLocation[3] - 5) // 2,
                text = app.menuPCX, fill = 'black', anchor = 'e')
    canvas.create_rectangle(submitButtonCX - submitButtonWidth // 2,
            app.checkboxXLocation[1],
            submitButtonCX + submitButtonWidth // 2,
            app.checkboxXLocation[3],
            fill = 'white', width = 3)
    canvas.create_text(submitButtonCX, 
            (app.checkboxXLocation[1] + app.checkboxXLocation[3]) // 2,
            text = 'Submit', font = 'Arial 17')

def drawYMenu(app, canvas, width, height, titleCX, textboxCX,
            submitButtonWidth, submitButtonHeight, submitButtonCX):
    canvas.create_text(titleCX, app.checkboxYLocation[1] - 10, 
            text = 'y: ', fill = 'white', 
            font = 'Arial 17', anchor = 'w')
    canvas.create_rectangle(app.checkboxYLocation[0],
            app.checkboxYLocation[1],
            app.checkboxYLocation[2],
            app.checkboxYLocation[3], fill = 'white')
    if app.menuSelected == 'y':
        canvas.create_line(app.checkboxYLocation[2] - 10,
                app.checkboxYLocation[1] + 5,
                app.checkboxYLocation[2] - 10,
                app.checkboxYLocation[3] - 5, width = 2)
    if app.menuPCY != None:
        canvas.create_text(app.checkboxYLocation[2] - 12, 
                (app.checkboxYLocation[1] + 5 + app.checkboxYLocation[3] - 5) // 2,
                text = app.menuPCY, fill = 'black', anchor = 'e')
    canvas.create_rectangle(submitButtonCX - submitButtonWidth // 2,
            app.checkboxYLocation[1],
            submitButtonCX + submitButtonWidth // 2,
            app.checkboxYLocation[3],
            fill = 'white', width = 3)
    canvas.create_text(submitButtonCX, 
            (app.checkboxYLocation[1] + app.checkboxYLocation[3]) // 2,
            text = 'Submit', font = 'Arial 17')

def drawChargeMenu(app, canvas, width, height, titleCX, textboxCX,
            submitButtonWidth, submitButtonHeight, submitButtonCX):
    canvas.create_text(titleCX, app.checkboxChargeLocation[1] - 10, 
            text = 'Charge: ', fill = 'white', 
            font = 'Arial 17', anchor = 'w')
    canvas.create_rectangle(app.checkboxChargeLocation[0],
            app.checkboxChargeLocation[1],
            app.checkboxChargeLocation[2],
            app.checkboxChargeLocation[3], fill = 'white')
    if app.menuSelected == 'Charge':
        canvas.create_line(app.checkboxChargeLocation[2] - 10,
                app.checkboxChargeLocation[1] + 5,
                app.checkboxChargeLocation[2] - 10,
                app.checkboxChargeLocation[3] - 5, width = 2)
    if app.menuPCCharge != None:
        canvas.create_text(app.checkboxChargeLocation[2] - 12, 
                (app.checkboxChargeLocation[1] + 5 + 
                app.checkboxChargeLocation[3] - 5) // 2,
                text = app.menuPCCharge, fill = 'black', anchor = 'e')
    canvas.create_rectangle(submitButtonCX - submitButtonWidth // 2,
            app.checkboxChargeLocation[1],
            submitButtonCX + submitButtonWidth // 2,
            app.checkboxChargeLocation[3],
            fill = 'white', width = 3)
    canvas.create_text(submitButtonCX, 
            (app.checkboxChargeLocation[1] + app.checkboxChargeLocation[3]) // 2,
            text = 'Submit', font = 'Arial 17')

def drawVelocityDirectionMenu(app, canvas, width, height, titleCX, textboxCX,
            submitButtonWidth, submitButtonHeight, submitButtonCX):
    canvas.create_text(titleCX, app.checkboxVelocityDirectionLocation[1] - 10,
            text = 'Velocity Direction: ', fill = 'white', 
            font = 'Arial 17', anchor = 'w')
    canvas.create_rectangle(app.checkboxVelocityDirectionLocation[0],
            app.checkboxVelocityDirectionLocation[1],
            app.checkboxVelocityDirectionLocation[2],
            app.checkboxVelocityDirectionLocation[3], fill = 'white')
    if app.menuSelected == 'Velocity Direction':
        canvas.create_line(app.checkboxVelocityDirectionLocation[2] - 10,
                app.checkboxVelocityDirectionLocation[1] + 5,
                app.checkboxVelocityDirectionLocation[2] - 10,
                app.checkboxVelocityDirectionLocation[3] - 5, width = 2)
    if app.menuPCVelocityDirection != None:
        canvas.create_text(app.checkboxVelocityDirectionLocation[2] - 12, 
                (app.checkboxVelocityDirectionLocation[1] + 5 + 
                app.checkboxVelocityDirectionLocation[3] - 5) // 2,
                text = app.menuPCVelocityDirection, fill = 'black', 
                anchor = 'e')
    canvas.create_rectangle(submitButtonCX - submitButtonWidth // 2,
            app.checkboxVelocityDirectionLocation[1],
            submitButtonCX + submitButtonWidth // 2,
            app.checkboxVelocityDirectionLocation[3],
            fill = 'white', width = 3)
    canvas.create_text(submitButtonCX, (app.checkboxVelocityDirectionLocation[1] + 
            app.checkboxVelocityDirectionLocation[3])//2,  
            text = 'Submit', font = 'Arial 17')

# Draws the error message if possible
def drawErrorMessage(app, canvas):
    if app.errorMessage != None:
        textAndRectCX = app.width // 2
        textAndRectCY = app.height - 100
        textAndRectHeight = 30
        canvas.create_rectangle(textAndRectCX - app.errorMessageTextAndRectWidth // 2, 
                textAndRectCY - textAndRectHeight // 2,
                textAndRectCX + app.errorMessageTextAndRectWidth // 2,
                textAndRectCY + textAndRectHeight // 2,
                fill = app.errorMessageColor)
        canvas.create_text(textAndRectCX, textAndRectCY, text = app.errorMessage,
                anchor = 'center')

# Draws the point charges if possible
def drawPointCharges(app, canvas):
    for currentPC in app.allPointCharges:
        canvas.create_oval(currentPC.cx - app.pointChargeRadius,
                currentPC.cy - app.pointChargeRadius,
                currentPC.cx + app.pointChargeRadius,
                currentPC.cy + app.pointChargeRadius,
                fill = app.pcColor)
        canvas.create_text(currentPC.cx, currentPC.cy,
                text = currentPC.charge, fill = 'white')
        drawVelocity(app, canvas, currentPC)

def drawVelocity(app, canvas, currentPC):
    if currentPC.velocityDirection != None:
        if currentPC.velocityDirection == 'I' or currentPC.velocityDirection == 'O':
            determineBoundsAndDrawVelocityInOrOut(app, canvas, currentPC, 
                    currentPC.velocityDirection, app.velocityArrowColor)
        else:
            drawForceArrowInDirection(app, canvas, currentPC, 
                    currentPC.velocityDirection, app.velocityArrowColor, 
                    app.velocityArrowLength)

# only draw velocity in or out circle along x axis of point charge
def determineBoundsAndDrawVelocityInOrOut(app, canvas, currentPC, 
                    direction, arrowColor):
    forceCircleCX = (currentPC.cx - app.pointChargeRadius - 
            app.pcToForceCircleMargin * 2)
    forceCircleCY = currentPC.cy
    if isValidForceCircleLocation(app, forceCircleCX, forceCircleCY):
        drawForceCircleInOrOut(app, canvas, forceCircleCX, forceCircleCY, 
                direction, arrowColor)
        return
    
    forceCircleCX = (currentPC.cx + app.pointChargeRadius + 
            app.pcToForceCircleMargin * 2)
    drawForceCircleInOrOut(app, canvas, forceCircleCX, forceCircleCY, 
                direction, arrowColor)


def drawFieldorForceAdditionalItem(app, canvas, x0, y0, x1, y1, direction, color):
    angle = math.pi / 4
    if direction == 'I':
        crossMargin = 6
        canvas.create_line(x0 + crossMargin, y0 + crossMargin, 
                x1 - crossMargin, y1 - crossMargin, fill = 'white')
        canvas.create_line(x0 + crossMargin, y1 - crossMargin, 
                x1 - crossMargin, y0 + crossMargin, fill = 'white')
    elif direction == 'O':
        cx = (x0 + x1) // 2
        cy = (y0 + y1) // 2
        canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, fill = 'white')
    elif direction == 'R' or (isinstance(direction, list) and 
            len(direction) == 1 and direction[0] == 'R'):
        x0Arrow = x1 - app.optionShortLineArrowLength * math.cos(angle)
        yAArrow = y1 - app.optionShortLineArrowLength * math.sin(angle)
        yBArrow = y1 + app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(x0Arrow, yAArrow, x1, y1, x0Arrow, yBArrow, 
                fill = color, width = app.arrowThickness)
    elif direction == 'L' or (isinstance(direction, list) and 
            len(direction) == 1 and direction[0] == 'L'):
        x1Arrow = x0 + app.optionShortLineArrowLength * math.cos(angle)
        yAArrow = y1 - app.optionShortLineArrowLength * math.sin(angle)
        yBArrow = y1 + app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(x1Arrow, yAArrow, x0, y0, x1Arrow, yBArrow, 
                fill = color, width = app.arrowThickness)
    elif direction == 'U' or (isinstance(direction, list) and 
            len(direction) == 1 and direction[0] == 'U'):
        xAArrow = x0 - app.optionShortLineArrowLength * math.cos(angle)
        xBArrow = x0 + app.optionShortLineArrowLength * math.cos(angle)
        y1Arrow = y0 + app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(xAArrow, y1Arrow, x0, y0, xBArrow, y1Arrow, 
                fill = color, width = app.arrowThickness)
    elif direction == 'D' or (isinstance(direction, list) and 
            len(direction) == 1 and direction[0] == 'D'):
        xAArrow = x1 - app.optionShortLineArrowLength * math.cos(angle)
        xBArrow = x1 + app.optionShortLineArrowLength * math.cos(angle)
        y1Arrow = y1 - app.optionShortLineArrowLength * math.sin(angle)
        canvas.create_line(xAArrow, y1Arrow, x1, y1, xBArrow, y1Arrow, 
                fill = color, width = app.arrowThickness)
    # direction is 2D
    else:
        #TODO
        pass

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
                drawFieldorForceAdditionalItem(app, canvas, x0 + app.inOutSymbolMargin, 
                        y0 + app.inOutSymbolMargin, 
                        x1 - app.inOutSymbolMargin, 
                        y1 - app.inOutSymbolMargin, currentField.direction, 
                        None)
            else:
                canvas.create_line(x0, y0, x1, y1, fill = color,
                        width = app.arrowThickness)
                drawFieldorForceAdditionalItem(app, canvas, x0, y0, x1, y1, 
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
        x0 = app.draggingEField[0] - app.compassArrowLength // 2
        x1 = x0 + app.compassArrowLength
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
        x0 = app.draggingBField[0] - app.compassArrowLength // 2
        x1 = x0 + app.compassArrowLength
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

def drawOriginDot(app, canvas):
    graphicsX = Calculations.cartesianToGraphicsX(0, 
            app.width - app.userOptionsWidth)
    graphicsY = Calculations.cartesianToGraphicsY(0, app.height)
    canvas.create_oval(graphicsX - 2, graphicsY - 2, 
            graphicsX + 2, graphicsY + 2, fill = 'gray', width = 0)
    canvas.create_text(graphicsX + 11, graphicsY + 8, text = '(0, 0)',
            font = 'Arial 8', fill = 'gray')

def drawForceArrowInDirection(app, canvas, currentPC, direction, arrowColor,
                            arrowLength = None):
    if arrowLength == None:
        arrowLength = app.forceArrowLength
    if direction == 'U' or (isinstance(direction, list) and 
            len(direction) == 1 and direction[0] == 'U'):
        x0 = x1 = currentPC.cx
        y1 = currentPC.cy - app.pointChargeRadius
        y0 = y1 - arrowLength
        canvas.create_line(x0, y0, x1, y1, fill = arrowColor, 
                width = app.arrowThickness)
    elif direction == 'D' or (isinstance(direction, list) and 
            len(direction) == 1 and direction[0] == 'D'):
        x0 = x1 = currentPC.cx
        y0 = currentPC.cy + app.pointChargeRadius
        y1 = y0 + arrowLength
        canvas.create_line(x0, y0, x1, y1, fill = arrowColor,
                width = app.arrowThickness)
    elif direction == 'R' or (isinstance(direction, list) and 
            len(direction) == 1 and direction[0] == 'R'):
        y0 = y1 = currentPC.cy
        x0 = currentPC.cx + app.pointChargeRadius
        x1 = x0 + arrowLength
        if x1 > app.width - app.userOptionsWidth:
            x1 = app.width - app.userOptionsWidth
            canvas.create_line(x0, y0, x1, y1, fill = arrowColor,
                    width = app.arrowThickness)
            return
        canvas.create_line(x0, y0, x1, y1, fill = arrowColor,
                    width = app.arrowThickness)
    elif direction == 'L' or (isinstance(direction, list) and 
            len(direction) == 1 and direction[0] == 'L'):
        y0 = y1 = currentPC.cy
        x1 = currentPC.cx - app.pointChargeRadius
        x0 = x1 - arrowLength
        canvas.create_line(x0, y0, x1, y1, fill = arrowColor,
                width = app.arrowThickness)
    #TODO: current version only handles XY plane
    elif isinstance(direction, list) and len(direction) > 1:
        radiansAngle = math.radians(direction[1])
        if direction[0] == 'R':
            dx0 = app.pointChargeRadius * math.cos(radiansAngle)
            dx1 = arrowLength * math.cos(radiansAngle)
        else:
            dx0 = -app.pointChargeRadius * math.cos(radiansAngle)
            dx1 = -arrowLength * math.cos(radiansAngle)
        if direction[2] == 'U':
            dy0 = -app.pointChargeRadius * math.sin(radiansAngle)
            dy1 = -arrowLength * math.sin(radiansAngle)
        else:
            dy0 = app.pointChargeRadius * math.sin(radiansAngle)
            dy1 = arrowLength * math.sin(radiansAngle)
        x0 = currentPC.cx + dx0
        y0 = currentPC.cy + dy0
        x1 = x0 + dx1
        y1 = y0 + dy1
        canvas.create_line(x0, y0, x1, y1, fill = arrowColor,
                width = app.arrowThickness)
    else:
        determineBoundsAndDrawForceInOrOut(app, canvas, currentPC, 
                direction, arrowColor)
        return
    
    drawFieldorForceAdditionalItem(app, canvas, x0, y0, x1, y1, direction, arrowColor)

def convertDirectionToLorRFirstXD(direction):
    result = []
    result.append(direction[0])
    result.append(int(direction[1]))
    if direction[2].isdigit():
        result[1] = result[1]*10 + int(direction[2])
        result.append(direction[3])
    else:
        result.append(direction[2])
    
    if result[0] == 'L' or result[0] == 'R':
        return result
    # swap the directions
    result[0], result[2] = result[2], result[0]
    # save angle as 90 minus the angle
    result[1] = 90 - result[1]
    return result

def determineBoundsAndDrawForceInOrOut(app, canvas, currentPC, direction, 
                                        arrowColor):
    forceCircleCX = currentPC.cx - app.pointChargeRadius - app.pcToForceCircleMargin
    forceCircleCY = currentPC.cy - app.pointChargeRadius - app.pcToForceCircleMargin
    if isValidForceCircleLocation(app, forceCircleCX, forceCircleCY):
        drawForceCircleInOrOut(app, canvas, forceCircleCX, forceCircleCY, 
                direction, arrowColor)
        return
    
    forceCircleCX = currentPC.cx + app.pointChargeRadius + app.pcToForceCircleMargin
    if isValidForceCircleLocation(app, forceCircleCX, forceCircleCY):
        drawForceCircleInOrOut(app, canvas, forceCircleCX, forceCircleCY, 
                direction, arrowColor)
        return
    
    forceCircleCX = currentPC.cx - app.pointChargeRadius - app.pcToForceCircleMargin
    forceCircleCY = currentPC.cy + app.pointChargeRadius + app.pcToForceCircleMargin
    if isValidForceCircleLocation(app, forceCircleCX, forceCircleCY):
        drawForceCircleInOrOut(app, canvas, forceCircleCX, forceCircleCY, 
                direction, arrowColor)
        return

    forceCircleCX = currentPC.cx + app.pointChargeRadius + app.pcToForceCircleMargin
    drawForceCircleInOrOut(app, canvas, forceCircleCX, forceCircleCY, 
                direction, arrowColor)

def drawForceCircleInOrOut(app, canvas, forceCircleCX, forceCircleCY, direction, 
                            arrowColor):
    canvas.create_oval(forceCircleCX - app.forceCircleRadius,
            forceCircleCY - app.forceCircleRadius,
            forceCircleCX + app.forceCircleRadius,
            forceCircleCY + app.forceCircleRadius,
            fill = arrowColor)
    if direction == 'I':
        crossLength = 3
        canvas.create_line(forceCircleCX - crossLength, 
                forceCircleCY - crossLength, 
                forceCircleCX + crossLength, 
                forceCircleCY + crossLength, fill = 'white')
        canvas.create_line(forceCircleCX + crossLength, 
                forceCircleCY - crossLength, 
                forceCircleCX - crossLength, 
                forceCircleCY + crossLength, fill = 'white')
    else:
        canvas.create_oval(forceCircleCX - 2, forceCircleCY - 2, 
                forceCircleCX + 2, forceCircleCY + 2, fill = 'white')

def isValidForceCircleLocation(app, cx, cy):
    if cx - app.forceCircleRadius < 0:
        return False
    if cx + app.forceCircleRadius >= app.width - app.userOptionsWidth:
        return False
    if cy - app.forceCircleRadius < 0:
        return False
    if cy + app.forceCircleRadius >= app.height:
        return False
    return True

def drawForceArrow(app, canvas, currentPC, direction, arrowColor, isElectric):
    if isElectric:
        if currentPC.charge == '-':
            direction = PointChargeClass.PointCharge.getOppositeDirection(direction)
        drawForceArrowInDirection(app, canvas, currentPC, direction, arrowColor)
    else:
        #TODO: draw magnetic forces
        pass

def draw1FieldForce(app, canvas, currentPC, currentField):
    if isinstance(currentField, EFieldClass.EField):
        drawForceArrow(app, canvas, currentPC, currentField.direction, 
                app.eForceArrowColor, True)
    else:
        drawForceArrow(app, canvas, currentPC, currentField.direction, 
                app.bForceArrowColor, False)

def drawFieldForces(app, canvas):
    for currentPC in app.allPointCharges:
        for currentEField in app.allEFields:
            draw1FieldForce(app, canvas, currentPC, currentEField)
        for currentBField in app.allBFields:
            draw1FieldForce(app, canvas, currentPC, currentBField)

def drawPCInteractions(app, canvas):
    if not app.showPCInteractions:
        return
    
    for pcEffected in app.allPointCharges:
        for pcCause in app.allPointCharges:
            if pcEffected == pcCause:
                continue
            
            bearing = Calculations.calculateBearingAngleBetween(pcEffected.cx, 
                    pcEffected.cy, pcCause.cx, pcCause.cy)
            if pcCause.charge == pcEffected.charge:
                bearing = Calculations.calculateOppositeBearingAngle(bearing)
            drawForceArrowInDirection(app, canvas, pcEffected, bearing, 
                    app.pcEForceArrowColor, app.pcForceArrowLength)
