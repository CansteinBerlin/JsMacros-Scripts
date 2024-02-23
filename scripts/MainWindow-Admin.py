

if __name__ == "": 
    from JsMacrosAC import *
    from .utils.widgets import *
    
# Handle and import methods from other folders
import sys
sys.path.insert(1, file.getParent() + "/utils")
from widgets import *

# Save Gui scale for later usage
guiScale = Client.getGameOptions().getVideoOptions().getGuiScale()
screens = {"Plot Gui": "plotsgui.py", "Allgemeine Gui": "generalgui.py"}

def openWindow(guiName):
    Hud.getOpenScreen().close()
    GlobalVars.putString("currentOpenScreen", guiName)
    JsMacros.runScript(file.getParent() + "/" + screens[guiName])

def init(screen):
    width = screen.getWidth()
    height = screen.getHeight()
    
    fifthWidth = width / 5
    thirdHeight = height / 3
    screen.addButton(fifthWidth, thirdHeight, fifthWidth, thirdHeight, "Plot Gui", 
                     JavaWrapper.methodToJava(lambda btn, _: openWindow("Plot Gui")))
    
    screen.addButton(fifthWidth * 3, thirdHeight, fifthWidth, thirdHeight, "Allgemeine Gui", 
                     JavaWrapper.methodToJava(lambda btn, _: openWindow("Allgemeine Gui")))
    
    

def onClose(screen):
    Client.getGameOptions().getVideoOptions().setGuiScale(guiScale)
    pass


currentScreen = GlobalVars.getString("currentOpenScreen")

if currentScreen == None: 
    # Create and Display Screen
    Chat.log("OpenScreen")
    Client.getGameOptions().getVideoOptions().setGuiScale(2)
    screen = Hud.createScreen("Canstein Admin Tools", False)
    screen.setOnInit(JavaWrapper.methodToJava(init))
    screen.setOnClose(JavaWrapper.methodToJava(onClose))
    Hud.openScreen(screen)
    
else:
    if currentScreen in screens.keys():
        JsMacros.runScript(file.getParent() + "/" + screens[currentScreen])