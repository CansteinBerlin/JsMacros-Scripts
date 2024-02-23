if __name__ == "": 
    from JsMacrosAC import *
    from ..utils.widgets import *
    
# Handle and import methods from other folders
import sys
sys.path.insert(1, file.getParentFile().getParent() + "/utils")
from widgets import *

# Sizes of different buttons etc.
CHECKBOX_SIZE = 20
ONLINE_MARKER_HEIGHT = 4
ONLINE_MARKER_WIDTH_ADDITION = 0
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
CANSTEIN_ACCOUNTS = 15
ONLINE_COLOR = 0x00ff00
OFFLINE_COLOR = 0xff0000

# Save Gui scale for later usage
guiScale = Client.getGameOptions().getVideoOptions().getGuiScale()

def runCommand(command):
    Chat.say(command)

# Main Gui Creation
def init(screen):
    width = screen.getWidth()
    height = screen.getHeight()
    
    ############## Gamemode Switcher ##############
    # Title:
    currentYPos = textWithLine(screen, "Gamemode Switcher:", TEXT_INDENT_X, CANSTEIN_ACCOUNTS_Y)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Buttons
    titles = ["Survival", "Creative", "Spectator"]
    actions = ["/gamemode 0", "/gamemode 1", "/gamemode 3"]
    buttons = []
    for index in range(len(actions)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(actions) + 1), BUTTON_HEIGHT, titles[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, screen: runCommand(actions[titles.index(btnHelper.getLabel().getString())])
        )))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Server Switcher ##############
    # Title:
    currentYPos = textWithLine(screen, "Server Switcher:", TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Buttons
    texts = ["Lobby Server", "Creative Server"]
    functions = [lambda: runCommand("/server lb"), lambda: runCommand("/server cr")]
    buttons = createMultipleButtonsWithDifferentFunctions(JavaWrapper, Chat, screen, texts, functions, currentYPos, width / (len(texts) + 1), BUTTON_HEIGHT)
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    
    
def onClose(screen):
    Client.getGameOptions().getVideoOptions().setGuiScale(guiScale)

# Create and Display Screen
Client.getGameOptions().getVideoOptions().setGuiScale(2)
screen = Hud.createScreen("PlotManager", False)
screen.setOnInit(JavaWrapper.methodToJava(init))
screen.setOnClose(JavaWrapper.methodToJava(onClose))
Hud.openScreen(screen)