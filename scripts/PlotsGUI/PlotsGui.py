if __name__ == "": 
    from JsMacrosAC import *
    from ..utils.widgets import *
    from ..utils.commands import *
    from ..utils.lang import Lang
    from ..utils.accounts import Accounts
    
# Handle and import methods from other folders
import sys
sys.path.insert(1, file.getParentFile().getParent() + "/utils")
from widgets import *
from commands import *
from lang import Lang
from accounts import Accounts

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
CANSTEIN_ACCOUNTS = 18
ONLINE_COLOR = 0x00ff00
OFFLINE_COLOR = 0xff0000
TOOLTIP_COLOR = "&7"

# This represents the canstein accounts that are enabled in the gui

# Functions TODO: FIX WITH PLAYER INPUT
def createPlotWithPlayers(textInput):
    Chat.say("/p auto")
    Client.waitTick(30)
    for i in range(10):
        Player.moveForward(0)
        Client.waitTick(1)
    
    Client.waitTick(10)
    Chat.say("/p middle")
    runSelfAllAccounts(Chat, accounts, textInput, "p trust %other%")
    runSelfAllAccounts(Chat, accounts, textInput, "p setowner %other%")
    Client.waitTick(20)
    
    runSelfAllAccounts(Chat, accounts, textInput, "tphere %other%")

def createPlotForAllPlayers(textInput):
    copy = list(accounts.selectedAccounts)
    for player in copy:
        accounts.selectedAccounts = []
        accounts.selectedAccounts.append(player)
        
        createPlotWithPlayers(textInput)
        Client.waitTick(30)
        
    accounts.selectedAccounts = copy


# Save Gui scale for later usage
guiScale = Client.getGameOptions().getVideoOptions().getGuiScale()

def back():
    Hud.getOpenScreen().close()
    GlobalVars.remove("currentOpenScreen")
    JsMacros.runScript(file.getParent() + "/" + "MainWindow-Admin.py")


# Main Gui Creation
def init(screen):
    width = screen.getWidth()
    
    ############## Canstein Account ##############
    # Title:
    currentYPos = textWithLine(screen, lang.get("accountSelectionTitle"), TEXT_INDENT_X, CANSTEIN_ACCOUNTS_Y)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Checkboxes
    checkboxes = []
    for i in range(CANSTEIN_ACCOUNTS):
        checkboxes.append(screen.addCheckbox(0, int(currentYPos), CHECKBOX_SIZE, CHECKBOX_SIZE, 0, str(i + 1), False, JavaWrapper.methodToJava(
            lambda btnHelper, screen: accounts.toggle(int(btnHelper.getLabel().getString()))
        )))
    checkboxes.append(screen.addCheckbox(0, int(currentYPos), CHECKBOX_SIZE, CHECKBOX_SIZE, 0, lang.get("selectAllAccounts"), False, JavaWrapper.methodToJava(
        lambda btnHelper, screen: accounts.setAll(btnHelper, checkboxes)            
    )))
    centerWidgets(screen, checkboxes)
    currentYPos += CHECKBOX_SIZE + OFFSET_Y_MARKER
    
    # If player not online disable checkboxes and display red Overlay 
    rects = []
    for i in range(CANSTEIN_ACCOUNTS):
        rects.append(screen.addRect(0, int(currentYPos), checkboxes[0].getWidth() + ONLINE_MARKER_WIDTH_ADDITION, currentYPos + ONLINE_MARKER_HEIGHT, ONLINE_COLOR, 255, 0, 1))
        if not ("Canstein" + str(i + 1)) in accounts.onlineAccounts:
            rects[i].setColor(OFFLINE_COLOR)
    rects.append(screen.addRect(0, int(currentYPos), checkboxes[0].getWidth() + ONLINE_MARKER_WIDTH_ADDITION, currentYPos + ONLINE_MARKER_HEIGHT, ONLINE_COLOR, 0, 0, 1))
    centerMultiposWidgets(screen, rects)
    
    # Player Input
    currentYPos += ONLINE_MARKER_HEIGHT + OFFSET_Y_ELEMENTS
    text = screen.addText(lang.get("playerInputField"), TEXT_INDENT_X, int(currentYPos + 5), 0xFFFFFF, False, 1, 0)
    textInput = screen.addTextInput(TEXT_INDENT_X + text.getWidth() + 20, int(currentYPos), TEXT_INPUT_WIDTH, BUTTON_HEIGHT, "", JavaWrapper.methodToJava(lambda string, screen: None))
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    
    ############## Player Plot Actions Line 1 ##############
    # Title:
    currentYPos = textWithLine(screen, lang.get("playerActionsTitle"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define Commands and titles 
    texts_1 = [lang.get("createPlotWithPlayers"), lang.get("add"), lang.get("trust"), lang.get("remove"), lang.get("deny")]
    actions_1 = [lang.get("createPlotWithPlayersTooltip"), "p add %other%", "p trust %other%", "p remove %other%", "p deny %other%"]
    
    # Create button plot create
    buttons = []
    buttons.append(screen.addButton(0, int(currentYPos), width // (len(texts_1) + 1), BUTTON_HEIGHT, texts_1[0], JavaWrapper.methodToJavaAsync(
            lambda _, __: createPlotWithPlayers(textInput.getText())
        )))
    buttons[0].addTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + actions_1[0]))
    
    # Create other buttons
    for index in range(1, len(texts_1)):
        buttons.append(screen.addButton(0, int(currentYPos), width // (len(texts_1) + 1), BUTTON_HEIGHT, texts_1[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, _: runSelfAllAccounts(Chat, accounts, textInput.getText(), actions_1[texts_1.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].addTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + "/" + actions_1[index]))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE

    ############## Single player plot actions ##############
    # Title:
    currentYPos = textWithLine(screen, lang.get("singlePlayerPlotActionsTitle"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    

    # Define Commands and titles
    texts_2 = [lang.get("setOwner"), lang.get("visit")]
    actions_2 = ["p setowner %other%", "p visit %other%"]
    
    # Create buttons
    buttons = []
    for index in range(len(actions_2)):
        buttons.append(screen.addButton(0, int(currentYPos), width // (len(actions_2) + 1), BUTTON_HEIGHT, texts_2[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, _: runFirstAccount(Chat, accounts, textInput.getText(), actions_2[texts_2.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].addTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + "/" + actions_2[index]))
    centerWidgets(screen, buttons)
    
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    
    ################ Plot Actions ################
    currentYPos = textWithLine(screen, lang.get("plotActionsTitle"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define Commands and titles
    texts_3 = [lang.get("plotInfo"), lang.get("claimPlot"), lang.get("deletePlot"), lang.get("markDone"), lang.get("continue")]
    actions_3 = ["/p info", "/p claim", "/p delete", "/p done", "/p continue"]
    
    # Create buttons
    buttons = []
    for index in range(len(actions_3)):
        buttons.append(screen.addButton(0, int(currentYPos), width // (len(actions_3) + 1), BUTTON_HEIGHT, texts_3[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, _: runCommand(Chat, actions_3[texts_3.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].addTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + actions_3[index]))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    #################### Misc ####################
    currentYPos = currentYPos = textWithLine(screen, lang.get("misc"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define Commands and titles
    texts_4 = [lang.get("createPlot"), lang.get("sendPlotId")]
    actions_4 = [lang.get("createPlotTooltip"), lang.get("sendPlotIdTooltip")]

    # Create buttons    
    buttons = []
    buttons.append(screen.addButton(0, int(currentYPos), width // (len(texts_4) + 1), BUTTON_HEIGHT, texts_4[0], JavaWrapper.methodToJavaAsync(
            lambda _, __: createPlotForAllPlayers(textInput.getText())
        )))
    buttons[0].addTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + actions_4[0]))
    
    buttons.append(screen.addButton(0, int(currentYPos), width // (len(texts_4) + 1), BUTTON_HEIGHT, texts_4[1], JavaWrapper.methodToJavaAsync(
            lambda _, __: runSelfAllAccounts(Chat, accounts, textInput.getText(), "/tm message -stay=150 %other% &6PlotID: %plotsquared_currentplot_xy%")
        )))
    buttons[0].addTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + actions_4[1]))

    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    #################### Close ####################
    # Close Gui
    closeButton = screen.addButton(20, screen.getHeight() - BUTTON_HEIGHT - 20, 100, BUTTON_HEIGHT, "Back", JavaWrapper.methodToJava(lambda _, __: back()))

def onClose(screen):
    Client.getGameOptions().getVideoOptions().setGuiScale(guiScale)

def main():
    global lang, accounts
    
    #Lang
    lang = Lang(Chat, file.getParent() + "/lang/" + file.getName().replace(".py", "") + ".lang")
    if not lang.load(): 
        Chat.log(Chat.createTextBuilder().append("Invalid or empty lang file").withColor(0xc).build())
        return
    # Accounts
    accounts = Accounts(World)
    
    # Create and Display Screen
    Client.getGameOptions().getVideoOptions().setGuiScale(2)
    screen = Hud.createScreen(lang.get("title"), False)
    screen.setOnInit(JavaWrapper.methodToJava(init))
    screen.setOnClose(JavaWrapper.methodToJava(onClose))
    Hud.openScreen(screen)

if __name__ == "__main__":
    main()