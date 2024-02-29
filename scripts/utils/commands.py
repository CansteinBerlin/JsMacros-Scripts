def runCommand(Chat, command):
    Chat.say(command)
    
def getPlayerString(accounts, inputText):
    playerString = ""
    for player in accounts.selectedAccounts:
        playerString += "Canstein" + str(player) + " "
    if len(inputText) > 0:
        playerString += str(inputText) + " "
    return playerString.strip()

def runSelfAllAccounts(Chat, accounts, inputText, command):
    playerString = getPlayerString(accounts, inputText)
    if len(playerString) == 0: return
    
    Chat.say("/runcommand self \"" + command + "\" " + playerString)
    Chat.log("/runcommand self \"" + command + "\" " + playerString)
    
def runOtherAllAccounts(Chat, accounts, inputText, command):
    playerString = getPlayerString(accounts, inputText)
    if len(playerString) == 0: return
    
    Chat.say("/runcommand other \"" + command + "\" " + playerString)
    
def runFirstAccount(Chat, accounts, inputText, command):
    player = ""
    if len(inputText) > 0 or len(accounts.selectedAccounts) == 0: player = inputText
    else: player = "Canstein" + str(accounts.selectedAccounts[0])
    if len(player) == 0: return
    
    Chat.say("/" + command.replace("%player%", player))
    
