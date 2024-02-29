import json

class Lang:
    def __init__(self, Chat, path):
        self.Chat = Chat
        self.path = path
    
    def load(self):    
        with open(self.path, "r") as langFile:
            try:
                self.langData = json.load(langFile)
            except:
                return False
        return True
                
    def get(self, key):
        if key in self.langData.keys(): 
            return self.Chat.ampersandToSectionSymbol(self.langData[key])
        return "UNKNOWN"