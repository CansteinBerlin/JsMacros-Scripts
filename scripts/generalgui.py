if __name__ == "": 
    from JsMacrosAC import *
    from .utils.widgets import *
    
# Handle and import methods from other folders
import sys
sys.path.insert(1, file.getParent() + "/utils")
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

# This represents the canstein accounts that are enabled in the gui
cansteinAccountsInWorld = []
markedCansteinAccounts = []

for player in World.getPlayers():
    if "Canstein" in player.getName():
        cansteinAccountsInWorld.append(player.getName())

def clickCansteinButton(account):
    if account in markedCansteinAccounts:
        markedCansteinAccounts.remove(account)
    else:
        markedCansteinAccounts.append(account)
        
def actionForAllSelectedPlayers(command, inputText):
    copy = command
    for player in markedCansteinAccounts:
        Chat.say(copy.replace("player", "Canstein" + str(player)))
    
    if len(inputText) > 0:
        Chat.say(copy.replace("player", inputText))

def actionForAllPlayers(command, inputText):
    copy = command
    for player in range(1, 16):
        Chat.say(copy.replace("player", "Canstein" + str(player)))
        Client.waitTick(1)
    
    if len(inputText) > 0:
        Chat.say(copy.replace("player", inputText))
    
# Save Gui scale for later usage
guiScale = Client.getGameOptions().getVideoOptions().getGuiScale()

def back():
    Hud.getOpenScreen().close()
    GlobalVars.remove("currentOpenScreen")
    JsMacros.runScript(file.getParent() + "/" + "MainWindow-Admin.py")

# Main Gui Creation
def init(screen):
    width = screen.getWidth()
    height = screen.getHeight()
    
    ############## Canstein Accounts And Player Input ##############
    # Title:
    currentYPos = textWithLine(screen, "Canstein Account selection and player input:", TEXT_INDENT_X, CANSTEIN_ACCOUNTS_Y)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Checkboxes
    buttons = []
    for i in range(CANSTEIN_ACCOUNTS):
        buttons.append(screen.addCheckbox(0, currentYPos, CHECKBOX_SIZE, CHECKBOX_SIZE, 0, str(i + 1), False, JavaWrapper.methodToJava(
            lambda btnHelper, screen: clickCansteinButton(int(btnHelper.getLabel().getString()))
        )))
    centerWidgets(screen, buttons)
    currentYPos += CHECKBOX_SIZE + OFFSET_Y_MARKER
    
    # If player not online disable checkboxes and display red Overlay 
    rects = []
    for i in range(CANSTEIN_ACCOUNTS):
        rects.append(screen.addRect(0, currentYPos, buttons[0].getWidth() + ONLINE_MARKER_WIDTH_ADDITION, currentYPos + ONLINE_MARKER_HEIGHT, ONLINE_COLOR, 255, 0, 1))
        if not ("Canstein" + str(i + 1)) in cansteinAccountsInWorld:
            rects[i].setColor(OFFLINE_COLOR)
    centerMultiposWidgets(screen, rects)
    
    # Player Input
    currentYPos += ONLINE_MARKER_HEIGHT + OFFSET_Y_ELEMENTS
    text = screen.addText("Player:", TEXT_INDENT_X, currentYPos + 5, 0xFFFFFF, False, 1, 0)
    textInput = screen.addTextInput(TEXT_INDENT_X + text.getWidth() + 20, currentYPos, TEXT_INPUT_WIDTH, BUTTON_HEIGHT, "", JavaWrapper.methodToJava(lambda string, screen: None))
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Allgemeine Aktionen ##############
    currentYPos = textWithLine(screen, "Allgemeine Aktionen (For all selected players)", TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Teleport to you
    texts = ["Teleport to you"]
    functions = [lambda: actionForAllSelectedPlayers("/tphere player", textInput.getText())]
    buttons = createMultipleButtonsWithDifferentFunctions(JavaWrapper, Chat, screen, texts, functions, currentYPos, width / (len(texts) + 1), BUTTON_HEIGHT)
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Send Befehle ##############
    currentYPos = textWithLine(screen, "Send to another server (For all selected players)", TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    texts_2 = ["Lobby", "Creative", "Events", "Survival", "Cooperation"]
    actions_2 = ["lb", "cr", "ev", "sv", "co"]
    buttons = []
    for index in range(len(actions_2)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(actions_2) + 1), BUTTON_HEIGHT, texts_2[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, _: actionForAllSelectedPlayers("/send player " + actions_2[texts_2.index(btnHelper.getLabel().getString())], textInput.getText())
        )))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Util Befehle ##############
    currentYPos = textWithLine(screen, "Util Commands (For all selected players)", TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    texts_3 = ["Mute", "Unmute", "Jail", "Unjail"]
    actions_3 = ["/mute player", "/unmute player", "/jail player 1h Stoeren der Arbeiten", "/unjail player"]
    buttons = []
    for index in range(len(texts_3)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(actions_3) + 1), BUTTON_HEIGHT, texts_3[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, _: actionForAllSelectedPlayers(actions_3[texts_3.index(btnHelper.getLabel().getString())], textInput.getText())
        )))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Aktions for all players Aktionen ##############
    currentYPos = textWithLine(screen, "Actions for all canstein accounts", TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Teleport to you
    texts = ["Teleport all to you", "Unmute all", "Mute all"]
    functions = [lambda: actionForAllPlayers("/tphere player", textInput.getText()), 
                 lambda: actionForAllPlayers("/unmute player", textInput.getText()),
                 lambda: actionForAllPlayers("/mute player", textInput.getText())]
    buttons = createMultipleButtonsWithDifferentFunctions(JavaWrapper, Chat, screen, texts, functions, currentYPos, width / (len(texts) + 1), BUTTON_HEIGHT)
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    # Close Gui
    closeButton = screen.addButton(20, screen.getHeight() - BUTTON_HEIGHT - 20, 100, BUTTON_HEIGHT, "Back", JavaWrapper.methodToJava(lambda _, __: back()))

def onClose(screen):
    Client.getGameOptions().getVideoOptions().setGuiScale(guiScale)

# Create and Display Screen
Client.getGameOptions().getVideoOptions().setGuiScale(2)
screen = Hud.createScreen("PlotManager", False)
screen.setOnInit(JavaWrapper.methodToJava(init))
screen.setOnClose(JavaWrapper.methodToJava(onClose))
Hud.openScreen(screen)