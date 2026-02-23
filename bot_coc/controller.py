########################
#   CLASS CONTROLLER   #
########################

class Controller:
    def __init__(self, view, bot):
        self.view = view
        self.bot = bot
        
    def AskChoice(self):
        while True:
            try:
                choix = int(input("Que souhaitez-vous faire ? "))
                return choix
            except ValueError:
                print("Entrée invalide ! Veuillez saisir un chiffre.")

    def CallView(self, message):
        self.view.ShowText(message)

    def CallCheckWindow(self):
        verif, text = self.bot.CheckWindow()
        if not verif:
            self.view.ShowText(text)
        return verif
            
    def RunProg(self):
        choix_bot = 100
        
        while(choix_bot != 9):
            self.view.Home()
            choix_bot = self.AskChoice()
            match choix_bot:
                case 1:
                    if(self.CallCheckWindow()):
                        self.bot.FarmMDO()
                case 2:
                    if(self.CallCheckWindow()):
                        self.bot.FarmPRINCIPAL()
                case 7:
                    if(self.CallCheckWindow()):
                        self.bot.SetZoom()
                case 8:
                    self.bot.DefineUserCoordinates(self.CallView)
                case 9:
                    print("Merci d'avoir utiliser le bot !")
                    print("A une prochaine !")