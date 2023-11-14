if __name__ == "": 
    from JsMacrosAC import *

markedCansteinAccounts = []

def createPlotWithPlayers():
    Chat.say("/p auto")
    Client.waitTick(20)
    for i in range(10):
        Player.moveForward(0)
        Client.waitTick(1)
    
    actionPlayerInPlot("add")
    Chat.say("/p setowner ServerInfo")
    Client.waitTick(20)
    
    for player in markedCansteinAccounts:
       Chat.say("/tphere Canstein" + str(player))

def actionPlayerInPlot(action):
    for player in markedCansteinAccounts:
        Chat.say("/p " + action + " Canstein" + str(player))
        Client.waitTick(5)
    
def actionInPlot(action):
    Chat.say("/p " + action)

def playerSpecificActionInPlot(action, player):
    Chat.say("/p " + action + " " + player)


def clickCansteinButton(btn, account):
    if account in markedCansteinAccounts:
        markedCansteinAccounts.remove(account)
    else:
        markedCansteinAccounts.append(account)
def init(screen):
    width = screen.getWidth()
    height = screen.getHeight()

    y = 50
    ############## Canstein Account ##############
    # Title:
    screen.addText("Canstein Accounts:", 30, y, 0xFFFFFF, False, 1.2, 0)
    y += 13
    # Line: 
    screen.addLine(0, y, width, y, 0xEEEEEE)
    y += 6
    # Buttons
    cx = 0
    bwidth = bheight = 20
    dist = width / 13
    for i in range(13):
        screen.addCheckbox(cx + (dist - bwidth) / 2, y, bwidth, bheight, str(i + 1), False, JavaWrapper.methodToJava(
            lambda btnHelper, screen: clickCansteinButton(btnHelper, int(btnHelper.getLabel().getString()))))
        cx += dist
    y += bheight + 15

    bwidth = (width - 5) / 5
    bbw = width / 4 
    cx = 0
    #Create Plot with Players
    screen.addButton(cx + (bbw - bwidth) / 2, y, bwidth, 25, "Create plot with players", JavaWrapper.methodToJavaAsync(
        lambda btnHelper, screen: createPlotWithPlayers()
    ))
    cx += bbw

    #Add players to plot
    screen.addButton(cx + (bbw - bwidth) / 2, y, bwidth, 25, "Add players to plot", JavaWrapper.methodToJavaAsync(
        lambda btnHelper, screen: actionPlayerInPlot("add")
    ))
    cx += bbw

    #Trust players to plot
    screen.addButton(cx + (bbw - bwidth) / 2, y, bwidth, 25, "Trust players to plot", JavaWrapper.methodToJavaAsync(
        lambda btnHelper, screen: actionPlayerInPlot("trust")
    ))
    cx += bbw

    #Remove Players from plot
    screen.addButton(cx + (bbw - bwidth) / 2, y, bwidth, 25, "Remove players from plot", JavaWrapper.methodToJavaAsync(
        lambda btnHelper, screen: actionPlayerInPlot("remove")
    ))


    y += bheight + 25

    ############## Plot Actions ##############
    # Title:
    screen.addText("Plot Actions:", 30, y, 0xFFFFFF, False, 1.2, 0)
    y += 13
    # Line: 
    screen.addLine(0, y, width, y, 0xEEEEEE)
    y += 10
    
    actions = ["info", "claim", "delete", "done", "continue"]
    titles = ["Plot Info", "Claim Plot", "Delete Plot", "Mark Done", "Continue"]
    bwidth = (width - 5) / (len(actions) + 1)
    bbw = width / len(actions)
    cx = 0
    for index in range(len(actions)):
        screen.addButton(cx + (bbw - bwidth) / 2, y, bwidth, 25, titles[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, screen: actionInPlot(actions[titles.index(btnHelper.getLabel().getString())])
        ))
        cx += bbw
    y += bheight + 25

    ############## Player Specific Actions ##############
    # Title:
    screen.addText("Plot Actions:", 30, y, 0xFFFFFF, False, 1.2, 0)
    y += 13
    # Line: 
    screen.addLine(0, y, width, y, 0xEEEEEE)
    y += 10
    # Input
    text = screen.addText("Player:", 30, y + 5, 0xFFFFFF, False, 1, 0)
    textInput = screen.addTextInput(30 + text.getWidth() + 20, y, 200, 20, "", JavaWrapper.methodToJava(lambda string, screen: None))
    y += 30
    #Buttons
    actions_2 = ["add", "trust", "setowner", "remove", "deny", "visit"]
    titles_2 = ["Add", "Trust", "SetOwner", "Remove", "Deny", "Visit"]
    bwidth = (width - 5) / (len(actions_2) + 1)
    bbw = width / len(actions_2)
    cx = 0
    for index in range(len(actions_2)):
        screen.addButton(cx + (bbw - bwidth) / 2, y, bwidth, 25, titles_2[index], JavaWrapper.methodToJavaAsync(
            lambda btnHelper, screen: playerSpecificActionInPlot(actions_2[titles_2.index(btnHelper.getLabel().getString())], textInput.getText())
        ))
        cx += bbw

screen = Hud.createScreen("PlotManager", False)
screen.setOnInit(JavaWrapper.methodToJava(init))
Hud.openScreen(screen)