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
                self.view.ShowText("Entrée invalide ! Veuillez saisir un chiffre.")

    def CallView(self, message):
        self.view.ShowText(message)

    def CallCheckSettings(self):
        verif, text = self.bot.CheckSettings()
        if not verif:
            self.view.ShowText(text)
        return verif
            
    def RunProg(self):
        choix_bot = 100
        choix_settings = 100
        
        while(choix_bot != 9):
            self.view.Home()
            choix_bot = self.AskChoice()
            match choix_bot:
                case 1:
                    if(self.CallCheckSettings()):
                        self.bot.FarmMDO()
                case 2:
                    if(self.CallCheckSettings()):
                        self.bot.FarmPRINCIPAL()
                case 7:
                    if(self.CallCheckSettings()):
                        self.bot.SetZoom()
                case 8:
                    while(choix_settings != 9):
                        self.view.Settings()
                        choix_settings = self.AskChoice()
                        match choix_settings:
                            case 1:
                                self.bot.DefineUserCoordinates(self.CallView)
                            case 2:
                                choix_heroes_mdo = "z"
                                while(choix_heroes_mdo not in ("o", "n")):
                                    self.view.ShowText("Avez vous au moins un héro dans la MDO ? (o/n)")
                                    choix_heroes_mdo = input()
                                self.bot.DefineHereosMDO(choix_heroes_mdo)


                            case 3:
                                choix_heroes_main = 100
                                while(choix_heroes_main not in (0, 1,2,3,4)):
                                    self.view.ShowText("Combien de héros avez vous a disposition en attaque ? (0/1/2/3/4)")
                                    choix_heroes_main = int(input())
                                self.bot.DefineHereosMAIN(choix_heroes_main)
                            case 4:
                                choix_trp_event = "z"
                                while(choix_trp_event not in ("o", "n")):
                                    self.view.ShowText("Est-ce qu'il y a une troupe d'évènement ? (o/n)")
                                    choix_trp_event = input()
                                self.bot.DefineTrpEVENT(choix_trp_event)
                            case 5:
                                pass
                            case 9:
                                self.view.ShowText("Fin du paramétrage")

                    
                case 9:
                    self.view.ShowText("Merci d'avoir utiliser le bot !")
                    self.view.ShowText("A une prochaine !")