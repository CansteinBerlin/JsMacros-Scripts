if __name__ == "": 
    from JsMacrosAC import *
    from ..utils.widgets import *
    from ..utils.commands import *
    from ..utils.lang import Lang
    
# Handle and import methods from other folders
import sys
sys.path.insert(1, file.getParentFile().getParent() + "/utils")
from widgets import *
from widgets import *
from commands import *
from lang import Lang

# Sizes of different buttons etc.
BUTTON_HEIGHT = 20
TEXT_INPUT_WIDTH = 200

# Specific not centered x positions
TEXT_INDENT_X = 30

# Y Positions of different Rows

CANSTEIN_ACCOUNTS_Y = 50
OFFSET_Y_ELEMENTS = 7
OFFSET_Y_MARKER = 3
OFFSET_Y_TITLE = 25

# Data
TOOLTIP_COLOR = "&7"

# Save Gui scale for later usage
guiScale = Client.getGameOptions().getVideoOptions().getGuiScale()

# Main Gui Creation
def init(screen):
    width = screen.getWidth()
    height = screen.getHeight()
    
    ############## Gamemode Switcher ##############
    # Title:
    currentYPos = textWithLine(screen, lang.get("gamemodeSwitchTitle"), TEXT_INDENT_X, CANSTEIN_ACCOUNTS_Y)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define commands and texts
    texts_1 = [lang.get("survival"), lang.get("creative"), lang.get("spectator")]
    actions_1 = ["/gamemode 0", "/gamemode 1", "/gamemode 3"]
    buttons = []
    
    # Create buttons
    for index in range(len(actions_1)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(actions_1) + 1), BUTTON_HEIGHT, texts_1[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, screen: runCommand(Chat, actions_1[texts_1.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].setTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + actions_1[index]))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Server Switcher ##############
    # Title:
    currentYPos = textWithLine(screen, lang.get("serverSwitcherTitle"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define Commands and texts
    texts_2 = [lang.get("lobbyServer"), lang.get("creativeServer")]
    actions_2 = ["/server lb", "/server ps"]
    
    # Create buttons
    buttons = []
    for index in range(len(actions_2)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(actions_2) + 1), BUTTON_HEIGHT, texts_2[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, screen: runCommand(Chat, actions_2[texts_2.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].setTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + actions_2[index]))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Builder Utilities ##############
    # Title:
    currentYPos = textWithLine(screen, lang.get("misc"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define commands and texts
    texts_3 = [lang.get("specialBlocks"), lang.get("toggleflight")]
    actions_3 = ["/bu special", "/toggleflight"]
    
    # Create buttons
    buttons = []
    for index in range(len(actions_3)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(actions_3) + 1), BUTTON_HEIGHT, texts_3[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, screen: runCommand(Chat, actions_3[texts_3.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].setTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + actions_3[index]))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
def onClose(screen):
    Client.getGameOptions().getVideoOptions().setGuiScale(guiScale)

def main():
    global lang
    
    # Language
    lang = Lang(Chat, file.getParent() + "/lang/" + file.getName().replace(".py", "") + ".lang")
    if not lang.load():
        Chat.log(Chat.createTextBuilder().append("Invalid or empty lang file").withColor(0xc).build())
        return
    
    # Create and Display Screen
    Client.getGameOptions().getVideoOptions().setGuiScale(2)
    screen = Hud.createScreen(lang.get("title"), False)
    screen.setOnInit(JavaWrapper.methodToJava(init))
    screen.setOnClose(JavaWrapper.methodToJava(onClose))
    Hud.openScreen(screen)
    
if __name__ == "__main__":
    main()