class Data:
    def __init__(self, fichier:str, user:str="", text:str=""):
        self.fichier = fichier
        self.user = user
        self.text = text
    
    def log(self):
        fichier = open(file="data/" + self.fichier, mode="r")
        count = int(fichier.read()) + 1
        fichier.close()
        fichier = open(file="data/" + self.fichier, mode="w")
        fichier.write(str(count))
        fichier.close()
    
    def suggestion(self):
        fichier = open(file="data/" + self.fichier, mode="a")
        fichier.write(self.user + " : " + self.text + "\n")
        fichier.close()


        
    