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

# This represents the canstein accounts that are enabled in the gui
cansteinAccountsInWorld = []
markedCansteinAccounts = []

for player in World.getPlayers():
    if "Canstein" in player.getName():
        cansteinAccountsInWorld.append(player.getName())

# Functions
def createPlotWithPlayers():
    Chat.say("/p auto")
    Client.waitTick(30)
    for i in range(10):
        Player.moveForward(0)
        Client.waitTick(1)
    
    Client.waitTick(10)
    Chat.say("/p middle")
    actionPlayerInPlot("trust")
    Chat.say("/p setowner ServerInfo")
    Client.waitTick(20)
    
    for player in markedCansteinAccounts:
       Chat.say("/tphere Canstein" + str(player))

def createPlotForAllPlayers():
    global markedCansteinAccounts
    copy = list(markedCansteinAccounts)
    for player in copy:
        markedCansteinAccounts = []
        markedCansteinAccounts.append(player)
        
        createPlotWithPlayers()
        Client.waitTick(10)
        
    markedCansteinAccounts = copy
        

def actionPlayerInPlot(action):
    for player in markedCansteinAccounts:
        Chat.say("/p " + action + " Canstein" + str(player))
        Client.waitTick(5)
    
def actionInPlot(action):
    Chat.say("/p " + action)

def playerSpecificActionInPlot(action, player):
    Chat.say("/p " + action + " " + player)


def clickCansteinButton(account):
    if account in markedCansteinAccounts:
        markedCansteinAccounts.remove(account)
    else:
        markedCansteinAccounts.append(account)
    
# Save Gui scale for later usage
guiScale = Client.getGameOptions().getVideoOptions().getGuiScale()

def back():
    Hud.getOpenScreen().close()
    GlobalVars.remove("currentOpenScreen")
    JsMacros.runScript(file.getParentFile().getParent() + "/PlotsGUI/" + "MainWindow-Admin.py")


# Main Gui Creation
def init(screen):
    width = screen.getWidth()
    
    ############## Canstein Account ##############
    # Title:
    currentYPos = textWithLine(screen, "Canstein Accounts (Applies to all selected players):", TEXT_INDENT_X, CANSTEIN_ACCOUNTS_Y)
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
    currentYPos += ONLINE_MARKER_HEIGHT + OFFSET_Y_ELEMENTS
    
    # Create, add, trust, remove player buttons
    #texts = [getTextInitialWordBold(Chat, "Create plot with players"), getTextInitialWordBold(Chat, "Add players to plot"), getTextInitialWordBold(Chat, "Trust players to plot"), getTextInitialWordBold(Chat, "Remove players from plot")]
    texts = ["Create plot with players", "Add players to plot", "Trust players to plot", "Remove players from plot"]
    functions = [createPlotWithPlayers, lambda: actionPlayerInPlot("add"), lambda: actionPlayerInPlot("trust"), lambda: actionPlayerInPlot("remove")]
    buttons = createMultipleButtonsWithDifferentFunctions(JavaWrapper, Chat, screen, texts, functions, currentYPos, width / (len(texts) + 1), BUTTON_HEIGHT)
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    
    ################ Plot Actions ################
    currentYPos = textWithLine(screen, "Plot Actions (Applies to the plot you are on):", TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Buttons
    actions = ["info", "claim", "delete", "done", "continue"]
    titles = ["Plot Info", "Claim Plot", "Delete Plot", "Mark Done", "Continue"]
    buttons = []
    for index in range(len(actions)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(actions) + 1), BUTTON_HEIGHT, titles[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, screen: actionInPlot(actions[titles.index(btnHelper.getLabel().getString())])
        )))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ########### Player Specific Actions ##########
    currentYPos = textWithLine(screen, "Player specific Actions (Applies to the player typed into the box):", TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Input Line with text display
    text = screen.addText("Player:", TEXT_INDENT_X, currentYPos + 5, 0xFFFFFF, False, 1, 0)
    textInput = screen.addTextInput(TEXT_INDENT_X + text.getWidth() + 20, currentYPos, TEXT_INPUT_WIDTH, BUTTON_HEIGHT, "", JavaWrapper.methodToJava(lambda string, screen: None))
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_ELEMENTS
    
    # Buttons
    actions_2 = ["add", "trust", "setowner", "remove", "deny", "visit"]
    titles_2 = ["Add", "Trust", "SetOwner", "Remove", "Deny", "Visit"]
    buttons = []
    for index in range(len(actions_2)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(actions_2) + 1), BUTTON_HEIGHT, titles_2[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, screen: playerSpecificActionInPlot(actions_2[titles_2.index(btnHelper.getLabel().getString())], textInput.getText())
        )))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    #################### Misc ####################
    currentYPos = currentYPos = textWithLine(screen, "Misc (For every selected player seperately):", TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Add buttons
    texts = ["Create plot"]
    functions = [createPlotForAllPlayers]
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