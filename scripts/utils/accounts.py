class Accounts:
    def __init__(self, World):
        self.World = World
        
        self.selectedAccounts = []
        self.onlineAccounts = []
        
        for player in World.getPlayers():
            if "Canstein" in player.getName():
                self.onlineAccounts.append(player.getName())
    
    def toggle(self, index):
        if index in self.selectedAccounts:
            self.selectedAccounts.remove(index)
        else:
            self.selectedAccounts.append(index)
    
    def setAll(self, btnHelper, checkboxes):
        for btn in checkboxes:
            btn.setChecked(btnHelper.isChecked())