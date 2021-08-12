'''
William Tang (wyt)
Created 7/6/2021
'''

import PointChargeClass, EFieldClass, BFieldClass, Calculations, Drawer
from cmu_112_graphics_altered import *

# Sets the app constants
def setConstants(app):
    app.maxPointCharges = 10
    app.pointChargeRadius = 12
    app.displayMenuRectWidth = 250
    app.displayMenuRectHeight = 320
    app.menuExitDimensions = 20
    app.defaultWidth = app.width
    app.defaultHeight = app.height
    app.userOptionsWidth = app.height // 4
    app.boardWidth = app.width - app.userOptionsWidth
    app.optionsCX = app.width - app.userOptionsWidth // 2
    app.optionsDrawingWidth = int(app.userOptionsWidth * 0.8)

    app.pointChargeOptionYs = (110, 150)
    app.eFieldsOptionYs = (160, 200)
    app.bFieldsOptionYs = (210, 250)
    app.interactionsBetweenPCOptionYs = (260, 315)
    app.resetButtonOptionYs = (325, 365)
    marginBetweenResetAndHelp = 5
    app.resetButtonOptionXs = (app.optionsCX - app.optionsDrawingWidth // 2, 
        app.optionsCX - marginBetweenResetAndHelp)
    app.helpButtonOptionXs = (app.optionsCX + marginBetweenResetAndHelp, 
            app.optionsCX + app.optionsDrawingWidth // 2)
    app.showPCInteractions = False
    app.checkboxCX = app.optionsCX - app.optionsDrawingWidth // 3
    app.compassArrowLength = 30
    app.optionShortLineArrowLength = 15
    app.arrowThickness = 2 

    app.forceArrowLength = 60
    app.pcForceArrowLength = 50
    app.velocityArrowLength = 40
    app.pcColor = 'Black'
    app.eArrowColor = 'Dark Blue'
    app.bArrowColor = 'Dark Red'
    app.eForceArrowColor = 'Pink'
    app.bForceArrowColor = 'Maroon1'
    app.pcEForceArrowColor = 'Purple'
    app.velocityArrowColor = 'Orange'
    
    app.askCX = app.boardWidth // 2
    app.askCY = app.height // 2
    app.askWidth = 500
    app.askHeight = 250
    app.askSubmitXs = (app.askCX + 30, app.askCX + 120)
    app.askSubmitYs = (app.askCY + 10, app.askCY + 50)
    app.inOutSymbolMargin = 12

    app.submitButtonWidth = 80
    app.submitButtonHeight = 30

    app.deleteButtonWidth = 80
    app.deleteButtonHeight = 20
    app.pcToForceCircleMargin = 7
    app.forceCircleRadius = 7

    app.helpWidth = 650
    app.helpHeight = 600

    setHelp(app)

# Sets the constants for help
def setHelp(app):
    leftSide = app.askCX - app.helpWidth // 2
    rightSide = app.askCX + app.helpWidth // 2
    topSide = app.askCY - app.helpHeight // 2
    app.helpSeparatorLineX = leftSide + 150
    app.helpTitleCX = (app.helpSeparatorLineX + rightSide) // 2
    app.helpTitleCY = topSide + 25
    app.helpTextX = app.helpSeparatorLineX + 40
    app.helpTextYStart = topSide + 60
    app.helpPage = 1
    
    app.buttonMessages = ['Instructions\npage 1', 'Instructions\npage 2', 
            'Credits']
    app.helpButtonsWidth = (app.helpSeparatorLineX - leftSide) * 0.7
    app.helpButtonsHeight = 50
    app.helpButtonsCX = (app.helpSeparatorLineX + leftSide) // 2
    buttonTopMargin = 100
    app.helpButtonsCYs = (topSide + buttonTopMargin, 
            topSide + app.helpButtonsHeight + buttonTopMargin + 25)

# Sets the initial values for app
def appStarted(app):
    Calculations.writeToLogFile("\nStart\n")
    setConstants(app)
    reset(app)

# Resets all the app variables that will change
def reset(app):
    app.allPointCharges = []
    app.allEFields = []
    app.allBFields = []
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
    app.isHelp = False
    app.helpPageNum = 0

    app.askDataFieldDirection = None

    app.errorMessageColor = 'Pink'

    app.clickedCurrentPC = False
    
    resetMenuInfo(app)

# Resets all the information for the menu
def resetMenuInfo(app):
    app.displayMenu = None
    app.displayDraggingMenu = False
    app.displayMenuRectCX = None
    app.displayMenuRectCY = None

    app.submitButtonCX = None
    app.menuPCX = None
    app.menuPCY = None
    app.menuPCCharge = None
    app.menuPCVelocityDirection = None
    app.menuSelected = None
    app.checkboxXLocation = None
    app.checkboxYLocation = None
    app.checkboxChargeLocation = None
    app.checkboxVelocityDirectionLocation = None
    app.menuPointCharge = None
    app.deleteButtonCY = None

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
    if app.displayMenuRectCX + rectWidth // 2 >= app.boardWidth:
        app.displayMenuRectCX = app.displayMenu.cx - rectWidth / 2 - margin
    elif app.displayMenuRectCX - rectWidth // 2 < 0:
        app.displayMenuRectCX = app.displayMenu.cx + rectWidth / 2 - margin

    app.displayMenuRectCY = (app.displayMenu.cy - rectHeight // 2 - margin - 
                                radius)
    if app.displayMenuRectCY - rectHeight // 2 < 0:
        app.displayMenuRectCY = (app.displayMenu.cy + rectHeight // 2 + margin + 
                                radius)
    
    app.checkboxXLocation = (
            app.displayMenuRectCX - app.displayMenuRectWidth // 2 + 15,
            app.displayMenuRectCY - 55,
            app.displayMenuRectCX - app.displayMenuRectWidth // 2 + 135,
            app.displayMenuRectCY - 30)
    
    app.checkboxYLocation = (
            app.checkboxXLocation[0],
            app.displayMenuRectCY - 5,
            app.checkboxXLocation[2],
            app.displayMenuRectCY + 20)
    
    app.checkboxChargeLocation = (
            app.checkboxXLocation[0],
            app.displayMenuRectCY + 45,
            app.checkboxXLocation[2],
            app.displayMenuRectCY + 70)
    
    app.checkboxVelocityDirectionLocation = (
            app.checkboxChargeLocation[0],
            app.displayMenuRectCY + 95,
            app.checkboxChargeLocation[2],
            app.displayMenuRectCY + 120)
    
    titleCX = app.displayMenuRectCX - app.displayMenuRectWidth // 2 + 15
    textboxCX = titleCX + 60
    app.submitButtonCX = textboxCX + 110
    
    app.deleteButtonCY = app.displayMenuRectCY + 140
    app.deleteButtonLocation = (
            app.displayMenuRectCX - app.deleteButtonWidth // 2,
            app.deleteButtonCY - app.deleteButtonHeight // 2,
            app.displayMenuRectCX + app.deleteButtonWidth // 2,
            app.deleteButtonCY + app.deleteButtonHeight // 2)

# Check if clicked outside the menu
def checkClickedOutOfMenu(app, event):
    if app.displayMenu != None:
        menuCX, menuCY, menuWidth, menuHeight = Drawer.getMenuLocations(app)
        if not (menuCX - menuWidth//2 <= event.x <= menuCX + menuWidth//2 and 
                menuCY - menuHeight//2 <= event.y <= menuCY + menuHeight//2):
            app.displayMenu = None
            return False
        return True
    return False

# Check if clicked the exit of the menu
def checkClickedMenuExit(app, event):
    if app.displayMenu != None:
        menuCX, menuCY, menuWidth, menuHeight = Drawer.getMenuLocations(app)
        exitDimensions = app.menuExitDimensions
        if (menuCX + menuWidth // 2 - exitDimensions <= event.x <= 
                menuCX + menuWidth // 2 and 
                menuCY - menuHeight // 2 <= event.y <= 
                menuCY - menuHeight // 2 + exitDimensions):
            app.displayMenu = None
            return True
    return False

# Check if wants to exit out of ask
def checkClickedAskExit(app, event):
    exitDimensions = app.menuExitDimensions
    if (app.askCX + app.askWidth // 2 - exitDimensions <= event.x <=
            app.askCX + app.askWidth // 2 and
            app.askCY - app.askHeight // 2 <= event.y <=
            app.askCY - app.askHeight // 2 + exitDimensions):
        app.isAskDataForEField = False
        app.isAskDataForBField = False

# Checks if a direction is valid and not 2D
def isValidDirectionEntry(key):
    key = key.upper()
    return key in {'U', 'D', 'L', 'R', 'I', 'O'}

# Checks if the new location for a point charge is valid
def isValidPCRelocation(app, x, y, movingPC):
    if (0 > x - app.pointChargeRadius or 
            app.boardWidth <= x + app.pointChargeRadius):
        return 'Error 1'
    if (0 > y - app.pointChargeRadius or
            app.height <= y + app.pointChargeRadius):
        return 'Error 1'
    
    # check for collision except against movingPC
    for currentPC in app.allPointCharges:
        if currentPC == movingPC:
            continue
        if (distance(x, y, currentPC.cx, currentPC.cy) <= 
                2*app.pointChargeRadius):
            return 'Error 2'
    return 'Works'

# Checks if a string is parseable to int
def isStringParseableToInt(s):
    if s == '-' or s == '+':
        return False
    for index in range(0, len(s)):
        if not (s[index].isdigit() or (index == 0 and 
                (s[index] == '-' or s[index] == '+'))):
            return False
    return True

# Saves how to modify x, y, charge, or velocityDirection
#  for a point charge where necessary when typed
def keyPressed(app, event):
    if app.isAskDataForEField or app.isAskDataForBField:
        if event.key == 'Enter':
            shouldAskSubmit(app)
        elif event.key == 'Delete':
            if app.askDataFieldDirection != None:
                app.askDataFieldDirection = app.askDataFieldDirection[:-1]
        elif isValidDirectionEntry(event.key):
            app.askDataFieldDirection = event.key
        else:
            setErrorMessage(app, 'Please enter a valid direction.')
            app.askDataFieldDirection = None
    elif app.menuSelected == 'x':
        if event.key == 'Enter':
            if app.menuPCX != None and isStringParseableToInt(app.menuPCX):
                shouldMenuPCSubmit(app)
            else:
                setErrorMessage(app, 'Please enter a valid x.')
                app.menuPCX = None
        elif event.key == 'Delete':
            if app.menuPCX != None and app.menuPCX != '':
                app.menuPCX = app.menuPCX[:-1]
        elif (len(event.key) == 1 and event.key.isalnum() or 
                event.key == '+' or event.key == '-'):
            if app.menuPCX == None:
                app.menuPCX = ''
            app.menuPCX += event.key
    elif app.menuSelected == 'y':
        if event.key == 'Enter':
            if app.menuPCY != None and isStringParseableToInt(app.menuPCY):
                shouldMenuPCSubmit(app)
            else:
                setErrorMessage(app, 'Please enter a valid x.')
                app.menuPCY = None
        elif event.key == 'Delete':
            if app.menuPCY != None and app.menuPCY != '':
                app.menuPCY = app.menuPCY[:-1]
        elif (len(event.key) == 1 and event.key.isalnum() or 
                event.key == '+' or event.key == '-'):
            if app.menuPCY == None:
                app.menuPCY = ''
            app.menuPCY += event.key
    elif app.menuSelected == 'Charge':
        if event.key == 'Enter':
            if (app.menuPCCharge != None and 
                    (app.menuPCCharge == '+' or app.menuPCCharge == '-')):
                shouldMenuPCSubmit(app)
            else:
                setErrorMessage(app, 'Please enter a valid charge.')
                app.menuPCCharge = None
        elif event.key == 'Delete':
            if app.menuPCCharge != None and app.menuPCCharge != '':
                app.menuPCCharge = app.menuPCCharge[:-1]
        elif (len(event.key) == 1 and event.key.isalnum() or 
                event.key == '+' or event.key == '-'):
            if app.menuPCCharge == None:
                app.menuPCCharge = ''
            app.menuPCCharge += event.key
    elif app.menuSelected == 'Velocity Direction':
        if event.key == 'Enter':
            #TODO: error checking direction for 2d velocity direction
            if (app.menuPCVelocityDirection != None and 
                    isValidDirectionEntry(app.menuPCVelocityDirection)):
                shouldMenuPCSubmit(app)
            else:
                setErrorMessage(app, 'Please enter a valid velocity direction.')
                app.menuPCVelocityDirection = None
        elif event.key == 'Delete':
            if (app.menuPCVelocityDirection != None and 
                    app.menuPCVelocityDirection != ''):
                app.menuPCVelocityDirection = app.menuPCVelocityDirection[:-1]
        elif (len(event.key) == 1 and event.key.isalnum() or 
                event.key == '+' or event.key == '-'):
            if app.menuPCVelocityDirection == None:
                app.menuPCVelocityDirection = ''
            app.menuPCVelocityDirection += event.key

# Removes the error message after 3000 ms
def timerFired(app):
    if app.errorMessageTimer != None:
        app.errorMessageTimer += app.timerDelay
        if app.errorMessageTimer >= 3000:
            app.errorMessage = None
            app.errorMessageTimer = None

# Checks if clicked on any of the options except reset and help
def clickedInOptionPane(app, event):
    if(app.optionsCX - app.optionsDrawingWidth // 2 <= event.x <= 
            app.optionsCX + app.optionsDrawingWidth // 2):
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
            Calculations.writeToLogFile(f'Set interactions to ' + 
                    f'{app.showPCInteractions}\n')

#  Checks if a given field is already in a list
def hasDuplicateFieldInList(app, currentField, fieldList):
    for field in fieldList:
        if currentField == field:
            return True
    return False

# Returns the opposite field in a list given a field, if possible
def getOppositeFieldInList(app, currentField, fieldList):
    for field in fieldList:
        if (currentField.direction == 
                Calculations.getOppositeDirection(field.direction)):
            return field
    return None

# Modifies x, y, charge, or velocityDirection for a point charge 
#  where necessary
def shouldMenuPCSubmit(app):
    if app.menuSelected == 'x':
        cartesianX = Calculations.cartesianToGraphicsX(int(app.menuPCX), 
                app.boardWidth)
        doesWork = isValidPCRelocation(app, cartesianX, app.menuPointCharge.cy, 
                app.menuPointCharge)
        if doesWork == 'Works':
            app.menuPointCharge.cx = cartesianX
            tempIndex = app.allPointCharges.index(app.menuPointCharge) + 1
            graphicsCX = Calculations.graphicsToCartesianX(
                        app.menuPointCharge.cx, app.boardWidth)
            graphicsCY = Calculations.graphicsToCartesianY(
                        app.menuPointCharge.cy, app.height)
            Calculations.writeToLogFile(f'Moving point charge #{tempIndex} to ' + 
                    f'({graphicsCX}, {graphicsCY})\n')
            app.menuPCX = None
            setDisplayMenuInfo(app)
        elif doesWork == 'Error 1':
            setErrorMessage(app, 'Location out of bounds.')
        else:
            setErrorMessage(app, 'Location collides with another point charge.')

    elif app.menuSelected == 'y':
        cartesianY = Calculations.cartesianToGraphicsY(int(app.menuPCY), 
                app.height)
        doesWork = isValidPCRelocation(app, app.menuPointCharge.cx, cartesianY,
                app.menuPointCharge)
        if doesWork == 'Works':
            app.menuPointCharge.cy = cartesianY
            tempIndex = app.allPointCharges.index(app.menuPointCharge) + 1
            graphicsCX = Calculations.graphicsToCartesianX(
                        app.menuPointCharge.cx, app.boardWidth)
            graphicsCY = Calculations.graphicsToCartesianY(
                        app.menuPointCharge.cy, app.height)
            Calculations.writeToLogFile(f'Moving point charge #{tempIndex} to ' + 
                    f'({graphicsCX}, {graphicsCY})\n')
            app.menuPCY = None
            setDisplayMenuInfo(app)
        elif doesWork == 'Error 1':
            setErrorMessage(app, 'Location out of bounds.')
        else:
            setErrorMessage(app, 'Location collides with another point charge.')
    elif app.menuSelected == 'Charge':
        app.menuPointCharge.charge = app.menuPCCharge
        tempIndex = app.allPointCharges.index(app.menuPointCharge) + 1
        Calculations.writeToLogFile(f'Changed charge #{tempIndex} to ' + 
                f'{app.menuPCCharge}\n')
        app.menuPCCharge = None
    elif app.menuSelected == 'Velocity Direction':
        app.menuPointCharge.velocityDirection = (
                app.menuPCVelocityDirection.upper())
        tempIndex = app.allPointCharges.index(app.menuPointCharge) + 1
        Calculations.writeToLogFile(f'Changed velocity direction #{tempIndex} ' + 
                f'to {app.menuPCVelocityDirection.upper()}\n')
        app.menuPCVelocityDirection = None
    app.menuSelected = None

# Adds a BField to the list of all the BFields so that 
# the in and out BFields are drawn last
def addBFieldToBList(app, currentBField):
    for index in range(0, len(app.allBFields)):
        if (app.allBFields[index].direction != 'I' and
                app.allBFields[index].direction != 'O'):
            app.allBFields.insert(index, currentBField)
            return
    app.allBFields.append(currentBField)

# Checks if should set the ask information
def shouldAskSubmit(app):
    if app.askDataFieldDirection == None:
        setErrorMessage(app, 'Please enter a field direction.')
        return

    if app.isAskDataForEField:
        app.isAskDataForEField = False
        currentEField = EFieldClass.EField(app.askDataFieldDirection)
        oppositeField = getOppositeFieldInList(app, currentEField, 
                app.allEFields)
        if oppositeField != None:
            app.allEFields.remove(oppositeField)
            setErrorMessage(app, 'The same field in the opposite direction ' + 
                    'already exists, so both are deleted because their ' + 
                    'effects cancel.')
            app.errorMessageColor = 'Light green'
            app.errorMessageTextAndRectWidth = 640
        elif not hasDuplicateFieldInList(app, currentEField, app.allEFields):
            app.allEFields.append(currentEField)
            Calculations.writeToLogFile(f'Added EField in ' + 
                    f'{currentEField.direction}\n')
        else:
            setErrorMessage(app, 'This field already exists, so ' + 
                    'it will not be added to the simulation.')
            app.errorMessageColor = 'Light green'
    else:
        app.isAskDataForBField = False
        currentBField = BFieldClass.BField(app.askDataFieldDirection)
        oppositeField = getOppositeFieldInList(app, currentBField, 
                app.allBFields)
        if oppositeField != None:
            app.allBFields.remove(oppositeField)
            setErrorMessage(app, 'The same field in the opposite direction ' + 
                    'already exists, so both are deleted because their ' + 
                    'effects cancel.')
            app.errorMessageColor = 'Light green'
            app.errorMessageTextAndRectWidth = 640
        elif not hasDuplicateFieldInList(app, currentBField, app.allBFields):
            addBFieldToBList(app, currentBField)
            Calculations.writeToLogFile(f'Added BField in ' + 
                    f'{currentBField.direction}\n')
        else:
            setErrorMessage(app, 'This field already exists, so ' + 
                    'it will not be added to the simulation.')
            app.errorMessageColor = 'Light green'
    app.askDataFieldDirection = None

# Check if clicked on the submit button for ask
def checkClickedAskSubmit(app, event):
    if (app.askSubmitXs[0] <= event.x <= app.askSubmitXs[1] and
            app.askSubmitYs[0] <= event.y <= app.askSubmitYs[1]):
        shouldAskSubmit(app)

# Saves how to modify x, y, charge, or velocityDirection
#  for a point charge where necessary when clicked in the menu
def clickedInMenu(app, event):
    if app.displayDraggingMenu:
        return

    app.clickedCurrentPC = False
    if checkClickedMenuExit(app, event):
        return
    
    if (app.deleteButtonLocation[0] <= event.x <= 
            app.deleteButtonLocation[2] and
            app.deleteButtonLocation[1] <= event.y <= 
            app.deleteButtonLocation[3]):
        app.allPointCharges.remove(app.menuPointCharge)
        tempIndex = len(app.allPointCharges) + 1
        Calculations.writeToLogFile(f'Deleted point charge #{tempIndex}\n')
        resetMenuInfo(app)
        return

    if (app.checkboxXLocation[1] <= event.y <= 
            app.checkboxXLocation[3]):
        if (app.checkboxXLocation[0] <= event.x <= 
                app.checkboxXLocation[2]):
            app.menuSelected = 'x'
        elif (app.submitButtonCX - app.submitButtonWidth // 2 <= event.x <= 
                app.submitButtonCX + app.submitButtonWidth // 2):
            if app.menuSelected != 'x':
                return
            
            if app.menuPCX != None and isStringParseableToInt(app.menuPCX):
                shouldMenuPCSubmit(app)
            else:
                setErrorMessage(app, 'Please enter a valid x.')
                app.menuPCX = None
    elif (app.checkboxYLocation[1] <= event.y <= 
            app.checkboxYLocation[3]):
        if (app.checkboxYLocation[0] <= event.x <= 
                app.checkboxYLocation[2]):
            app.menuSelected = 'y'
        elif (app.submitButtonCX - app.submitButtonWidth // 2 <= event.x <= 
                app.submitButtonCX + app.submitButtonWidth // 2):
            if app.menuSelected != 'y':
                return
            
            if app.menuPCY != None and isStringParseableToInt(app.menuPCY):
                shouldMenuPCSubmit(app)
            else:
                setErrorMessage(app, 'Please enter a valid y.')
                app.menuPCY = None
    elif (app.checkboxChargeLocation[1] <= event.y <= 
            app.checkboxChargeLocation[3]):
        if (app.checkboxChargeLocation[0] <= event.x <= 
                app.checkboxChargeLocation[2]):
            app.menuSelected = 'Charge'
        elif (app.submitButtonCX - app.submitButtonWidth // 2 <= event.x <= 
                app.submitButtonCX + app.submitButtonWidth // 2):
            if app.menuSelected != 'Charge':
                return
            
            if (app.menuPCCharge != None and 
                    (app.menuPCCharge == '+' or app.menuPCCharge == '-')):
                shouldMenuPCSubmit(app)
            else:
                setErrorMessage(app, 'Please enter a valid charge.')
                app.menuPCCharge = None
    elif (app.checkboxVelocityDirectionLocation[1] <= event.y <= 
            app.checkboxVelocityDirectionLocation[3]):
        if (app.checkboxVelocityDirectionLocation[0] <= event.x <= 
                app.checkboxVelocityDirectionLocation[2]):
            app.menuSelected = 'Velocity Direction'
        elif (app.submitButtonCX - app.submitButtonWidth // 2 <= event.x <= 
                app.submitButtonCX + app.submitButtonWidth // 2):
            if app.menuSelected != 'Velocity Direction':
                return
            
            if (app.menuPCVelocityDirection != None and 
                    isValidDirectionEntry(app.menuPCVelocityDirection)):
                shouldMenuPCSubmit(app)
            else:
                setErrorMessage(app, 'Please enter a valid velocity direction.')
                app.menuPCVelocityDirection = None

# Checks if clicked in the help pane
def clickedInHelp(app, event):
    return (app.askCX - app.helpWidth // 2 <= event.x <= 
            app.askCX + app.helpWidth // 2 and 
            app.askCY - app.helpHeight // 2 <= event.y <= 
            app.askCY + app.helpHeight // 2)

# Checks if clicked on a specific button within the help pane
def doHelp(app, event):
    # clicked exit
    if (app.askCX + app.helpWidth // 2 - app.menuExitDimensions <= event.x <=
            app.askCX + app.helpWidth // 2 and 
            app.askCY - app.helpHeight // 2 <= event.y <=
            app.askCY - app.helpHeight // 2 + app.menuExitDimensions):
        app.isHelp = False
    
    if (app.helpButtonsCX - app.helpButtonsWidth // 2 <= event.x <=
            app.helpButtonsCX + app.helpButtonsWidth // 2):
        # clicked top button
        if (app.helpButtonsCYs[0] - app.helpButtonsHeight // 2 <= event.y <=
                app.helpButtonsCYs[0] + app.helpButtonsHeight // 2):
            app.helpPage = 2 if app.helpPage == 1 else 1
        # clicked bottom button
        elif (app.helpButtonsCYs[1] - app.helpButtonsHeight // 2 <= event.y <=
                app.helpButtonsCYs[1] + app.helpButtonsHeight // 2):
            app.helpPage = 2 if app.helpPage == 3 else 3

# Modifies game behavior in expected manner when the mouse is pressed down
def mousePressed(app, event):
    if (app.resetButtonOptionYs[0] <= event.y <= 
            app.resetButtonOptionYs[1]):
        if (app.resetButtonOptionXs[0] <= event.x <= 
                app.resetButtonOptionXs[1]):
            Calculations.writeToLogFile(f'Reset\n')
            reset(app)
            return
        elif (app.helpButtonOptionXs[0] <= event.x <= 
                app.helpButtonOptionXs[1]):
            app.isHelp = not app.isHelp
            return

    if app.isHelp:
        if clickedInHelp(app, event):
            doHelp(app, event)
        return

    if checkClickedOutOfMenu(app, event):
        clickedInMenu(app, event)
        return

    # clicked in option pane
    if event.x + app.pointChargeRadius >= app.boardWidth:
        clickedInOptionPane(app, event)
        return

    if app.isAskDataForEField or app.isAskDataForBField:
        checkClickedAskExit(app, event)
        checkClickedAskSubmit(app, event)
        return

    # check if clicked inside a point charge
    for currentPC in app.allPointCharges:
        if (currentPC.cx - app.pointChargeRadius <= event.x <= 
                currentPC.cx + app.pointChargeRadius and
                (currentPC.cy - app.pointChargeRadius <= event.y <= 
                currentPC.cy + app.pointChargeRadius)):
            app.displayMenu = currentPC
            setDisplayMenuInfo(app)
            app.menuPointCharge = currentPC
            app.clickedCurrentPC = True
            return

# Modifies game behavior in expected manner when the mouse is dragged
def mouseDragged(app, event):
    if app.isAskDataForEField or app.isAskDataForBField:
        return

    if (app.menuPointCharge != None and app.displayMenu != None and 
            app.clickedCurrentPC):
        if (isValidPCRelocation(app, event.x, event.y, app.menuPointCharge) == 
                'Works'):
            app.menuPointCharge.cx = event.x
            app.menuPointCharge.cy = event.y
            app.displayDraggingMenu = True
            setDisplayMenuInfo(app)
    elif app.draggingPCOption:
        app.draggingPC = (event.x, event.y)
    elif app.draggingEFieldOption:
        app.draggingEField = (event.x, event.y)
    elif app.draggingBFieldOption:
        app.draggingBField = (event.x, event.y)

# If allowed location, adds a point charge to the list of point charges
def addPC(app, event):
    if (event.x + app.pointChargeRadius >= app.boardWidth or 
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
    tempIndex = len(app.allPointCharges)
    Calculations.writeToLogFile(f'Added point charge #{tempIndex} at (' + 
            f'{Calculations.graphicsToCartesianX(event.x, app.boardWidth)}, ' + 
            f'{Calculations.graphicsToCartesianY(event.y, app.height)})\n')

# Modifies game behavior in expected manner when the mouse is released
def mouseReleased(app, event):
    app.displayDraggingMenu = False
    if (app.menuPointCharge != None and app.displayMenu != None and 
            app.clickedCurrentPC):
        app.clickedCurrentPC = False
        tempIndex = app.allPointCharges.index(app.menuPointCharge) + 1
        graphicsCX = Calculations.graphicsToCartesianX(
                app.menuPointCharge.cx, app.boardWidth)
        graphicsCY = Calculations.graphicsToCartesianY(
                app.menuPointCharge.cy, app.height)
        Calculations.writeToLogFile(f'Moved point charge #{tempIndex} to ' + 
                f'({graphicsCX}, {graphicsCY})\n')

    if app.draggingPCOption:
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
    app.errorMessageColor = 'Pink'
    # used for the error message
    app.errorMessageTextAndRectWidth = 400

# Draws everything
def redrawAll(app, canvas):
    Drawer.drawAll(app, canvas)

runApp(width = 1000, height = 700)