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
        
        
    def RunProg(self):
        choix_bot = 100
        
        while(choix_bot != 9):
            self.view.MenuPrincipal()
            choix_bot = self.AskChoice()
            match choix_bot:
                case 1:
                    self.bot.FarmMDO()
                case 2:
                    print("Choix 2")
                case 9:
                    print("Merci d'avoir utiliser le bot !")
                    print("A une prochaine !")