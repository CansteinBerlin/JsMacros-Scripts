if __name__ == "": 
    from JsMacrosAC import *
    from ..utils.widgets import *
    from ..utils.commands import *
    from ..utils.lang import Lang
    from ..utils.accounts import Accounts
    
# Handle and import methods from other folders
import sys
import json
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
CANSTEIN_ACCOUNTS = 15
ONLINE_COLOR = 0x00ff00
OFFLINE_COLOR = 0xff0000
TOOLTIP_COLOR = "&7"

# Save Gui scale for later usage
guiScale = Client.getGameOptions().getVideoOptions().getGuiScale()

def back():
    Hud.getOpenScreen().close()
    GlobalVars.remove("currentOpenScreen")
    JsMacros.runScript(file.getParentFile().getParent() + "/PlotsGUI/" + "MainWindow-Admin.py")
        

# Main Gui Creation
def init(screen):
    width = screen.getWidth()
    height = screen.getHeight()
    
    ############## Canstein Accounts And Player Input ##############
    # Title:
    currentYPos = textWithLine(screen, lang.get("accountSelectionTitle"), TEXT_INDENT_X, CANSTEIN_ACCOUNTS_Y)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Checkboxes
    checkboxes = []
    for i in range(CANSTEIN_ACCOUNTS):
        checkboxes.append(screen.addCheckbox(0, currentYPos, CHECKBOX_SIZE, CHECKBOX_SIZE, 0, str(i + 1), False, JavaWrapper.methodToJava(
            lambda btnHelper, screen: accounts.toggle(int(btnHelper.getLabel().getString()))
        )))
    checkboxes.append(screen.addCheckbox(0, currentYPos, CHECKBOX_SIZE, CHECKBOX_SIZE, 0, lang.get("selectAllAccounts"), False, JavaWrapper.methodToJava(
        lambda btnHelper, screen: accounts.setAll(btnHelper, checkboxes)            
    )))
    centerWidgets(screen, checkboxes)
    currentYPos += CHECKBOX_SIZE + OFFSET_Y_MARKER
    
    # If player not online disable checkboxes and display red Overlay 
    rects = []
    for i in range(CANSTEIN_ACCOUNTS):
        rects.append(screen.addRect(0, currentYPos, checkboxes[0].getWidth() + ONLINE_MARKER_WIDTH_ADDITION, currentYPos + ONLINE_MARKER_HEIGHT, ONLINE_COLOR, 255, 0, 1))
        if not ("Canstein" + str(i + 1)) in accounts.onlineAccounts:
            rects[i].setColor(OFFLINE_COLOR)
    rects.append(screen.addRect(0, currentYPos, checkboxes[0].getWidth() + ONLINE_MARKER_WIDTH_ADDITION, currentYPos + ONLINE_MARKER_HEIGHT, ONLINE_COLOR, 0, 0, 1))
    centerMultiposWidgets(screen, rects)
    
    # Player Input
    currentYPos += ONLINE_MARKER_HEIGHT + OFFSET_Y_ELEMENTS
    text = screen.addText(lang.get("playerInputField"), TEXT_INDENT_X, currentYPos + 5, 0xFFFFFF, False, 1, 0)
    textInput = screen.addTextInput(TEXT_INDENT_X + text.getWidth() + 20, currentYPos, TEXT_INPUT_WIDTH, BUTTON_HEIGHT, "", JavaWrapper.methodToJava(lambda string, screen: None))
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Allgemeine Aktionen ##############
    currentYPos = textWithLine(screen, lang.get("generalOptionsTitle"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define commands and titles
    texts_1 = [lang.get("teleportAction"), lang.get("muteAction"), lang.get("unmuteAction"), lang.get("jailAction"), lang.get("unjailAction")]
    actions_1 = ["tphere %other%", "mute %other%", "unmute %other%", "jail %other% 1h Auszeit!", "unjail %other%"]
    
    # Create Buttons 
    buttons = []
    for index in range(len(texts_1)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(texts_1) + 1), BUTTON_HEIGHT, texts_1[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, _: runSelfAllAccounts(Chat, accounts, textInput.getText(), actions_1[texts_1.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].addTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + "/" + actions_1[index]))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Send Befehle ##############
    currentYPos = textWithLine(screen, lang.get("sendServerTitle"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define commands and titles
    texts_2 = [lang.get("lobbyServer"), lang.get("creativeServer"), lang.get("eventServer"), lang.get("survivalServer"), lang.get("coopServer")]
    actions_2 = ["lb", "ps", "is", "sv", "co"]
    
    # Create buttons
    buttons = []
    for index in range(len(actions_2)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(actions_2) + 1), BUTTON_HEIGHT, texts_2[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, _: runSelfAllAccounts(Chat, accounts, textInput.getText(), "redcmdbukkit %other% server " + actions_2[texts_2.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].setTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + "/redcmdbukkit %other% server " + actions_2[index]))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Befehle fuer alle Spieler auf dem Server ##############
    currentYPos = textWithLine(screen, lang.get("utilCommandsTitle"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define commands and titles
    texts_3 = [lang.get("freezeAction"), lang.get("unfreezeAction"), lang.get("clearInvAction"), lang.get("ppoResetAction")]
    actions_3 = ["/freeze on -nothing false", "/freeze off", "/clear %other%", "/ppo %other% reset"]
    
    # Create buttons
    buttons = []
    for index in range(len(texts_3)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(actions_3) + 1), BUTTON_HEIGHT, texts_3[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, _: autoRunCommand(Chat, accounts, textInput.getText(), actions_3[texts_3.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].setTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + actions_3[index]))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE
    
    ############## Gamemode Changer ##############
    currentYPos = textWithLine(screen, lang.get("gamemodeTitle"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define commands and titles
    texts_1 = [lang.get("survivalGamemode"), lang.get("creativeGamemode"), lang.get("adventureGamemode"), lang.get("spectatorGamemode")]
    actions_1 = ["/gm 0 %other%", "/gm 1 %other%", "/gm 2 %other%", "/gm 3 %other%"]
    
    # Create Buttons 
    buttons = []
    for index in range(len(texts_1)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(texts_1) + 1), BUTTON_HEIGHT, texts_1[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, _: runSelfAllAccounts(Chat, accounts, textInput.getText(), actions_1[texts_1.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].addTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + actions_1[index]))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE

    ############## Player Utilities ##############
    currentYPos = textWithLine(screen, lang.get("playerUtilitiesTitle"), TEXT_INDENT_X, currentYPos)
    currentYPos += OFFSET_Y_ELEMENTS
    
    # Define commands and titles
    texts_1 = [lang.get("hidePlayers"), lang.get("showPlayers"), lang.get("resetRank")]
    actions_1 = ["/pd hide %other%", "/pd show %other%", "redcmdbukkit %self% lpb user %other% parent set mitglied || redcmdbukkit %self% lpb user %other% parent add canstein-rang"]
    
    # Create Buttons 
    buttons = []
    for index in range(len(texts_1)):
        buttons.append(screen.addButton(0, currentYPos, width / (len(texts_1) + 1), BUTTON_HEIGHT, texts_1[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, _: runMultipleSelfAllAccounts(Chat, Client, accounts, textInput.getText(), actions_1[texts_1.index(btnHelper.getLabel().getString())])
        )))
        buttons[index].addTooltip(Chat.ampersandToSectionSymbol(TOOLTIP_COLOR + actions_1[index]))
    centerWidgets(screen, buttons)
    currentYPos += BUTTON_HEIGHT + OFFSET_Y_TITLE

    ############## Close GUI ##############
    # Close Gui
    closeButton = screen.addButton(20, screen.getHeight() - BUTTON_HEIGHT - 20, 100, BUTTON_HEIGHT, lang.get("backButton"), JavaWrapper.methodToJava(lambda _, __: back()))

def onClose(screen):
    Client.getGameOptions().getVideoOptions().setGuiScale(guiScale)

def main():
    # Language
    global lang, accounts
    lang = Lang(Chat, file.getParent() + "/lang/" + file.getName().replace(".py", "") + ".lang")
    if not lang.load(): 
        Chat.log(Chat.createTextBuilder().append("Invalid or empty lang file").withColor(0xc).build())
        return

    # Accounts
    accounts = Accounts(World)

    # Create screen
    Client.getGameOptions().getVideoOptions().setGuiScale(2)
    screen = Hud.createScreen(lang.get("title"), False)
    screen.setOnInit(JavaWrapper.methodToJava(init))
    screen.setOnClose(JavaWrapper.methodToJava(onClose))
    Hud.openScreen(screen)


if __name__ == "__main__":
    main()