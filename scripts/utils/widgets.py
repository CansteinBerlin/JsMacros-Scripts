def centerWidgets(screen, elements):
    screenWidth = screen.getWidth()
    elementsWidth = 0
    for element in elements:
        elementsWidth += element.getWidth()
    
    widthBetweenElements = (screenWidth - elementsWidth) / (len(elements) + 1)
    
    xPos = widthBetweenElements
    for element in elements:
        element.setPos(xPos, element.getY())
        xPos += element.getWidth() + widthBetweenElements
        
def centerMultiposWidgets(screen, elements):
    screenWidth = screen.getWidth()
    elementsWidth = 0
    for element in elements:
        elementsWidth += element.getWidth()
    
    widthBetweenElements = (screenWidth - elementsWidth) / (len(elements) + 1)
    
    xPos = widthBetweenElements
    for element in elements:
        element.setPos(xPos, element.getY1(), xPos + element.getWidth(), element.getY2())
        xPos += element.getWidth() + widthBetweenElements

def textWithLine(screen, text, x, y):
    screen.addText(text, x, y, 0xFFFFFE, False, 1.2, 0)
    screen.addLine(0, y + 13, screen.getWidth(), y + 13, 0xFFFFFE)
    return y + 13
    
def createMultipleButtonsWithDifferentFunctions(JavaWrapper, Chat, screen, texts, functions, y, width, height):
    buttons = []
    for i in range(len(functions)):
        buttons.append(screen.addButton(0, y, width, height, texts[i], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, screen: functions[texts.index(btnHelper.getLabel().getString())]()
        )))
        buttons[i].setLabel(getTextInitialWordBold(Chat, texts[i]))
    return buttons

def getTextInitialWordBold(Chat, text):
    parts = text.split(" ")
    textbuilder = Chat.createTextBuilder()
    textbuilder.append(parts[0]).withFormatting(False, True, False, False, False).withColor(255, 170, 0)
    for i in range(1, len(parts)):
        textbuilder.append(" " + str(parts[i])).withFormatting(False, False, False, False, False)
    return textbuilder.build()