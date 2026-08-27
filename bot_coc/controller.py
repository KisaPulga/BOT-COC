########################
#   CLASS CONTROLLER   #
########################

from bot_coc.bot import Bot
import time

class Controller:
    def __init__(self, view):
        self.view = view
        self.bots = []

    def AskBotCount(self):
        while True:
            try:
                count = int(input("Combien d'instances souhaitez-vous lancer ? "))
                if count > 0:
                    return count
                print("Veuillez saisir un nombre supérieur à zéro.")
            except ValueError:
                print("Entrée invalide ! Veuillez saisir un chiffre.")

    def ConfigureBots(self):
        count = self.AskBotCount()
        self.bots = []

        for index in range(count):
            self.view.ShowText(f"\nParamétrage de l'instance {index + 1}/{count}")
            bot = Bot()
            bot.DefineUserCoordinates(self.CallView)
            self.bots.append(bot)
        
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
        all_valid = True
        for index, bot in enumerate(self.bots):
            verif, text = bot.CheckWindow()
            if not verif:
                self.view.ShowText(f"Instance {index + 1} : {text}")
                all_valid = False
        return all_valid

    def RunFarmPrincipal(self):
        compteur = 1
        while True:
            self.view.ShowText(f"\n===== Séquence {compteur} =====")
            features = [bot.farm_principal for bot in self.bots]

            self.view.ShowText("Étape 1/5 : lancement des attaques")
            for feature in features:
                feature.bot.ActivateWindow()
                feature.SetupPositions()
                feature.StartAttackSearch()

            self.view.ShowText("Étape 2/5 : vérification du pixel rouge")
            found_features = []
            for index, feature in enumerate(features):
                feature.bot.ActivateWindow()
                if feature.WaitForAttack():
                    self.view.ShowText(f"Instance {index + 1} : attaque trouvée")
                    found_features.append(feature)
                else:
                    self.view.ShowText(f"Instance {index + 1} : attaque non trouvée")
                    feature.CancelAttackSearch()

            self.view.ShowText("Étape 3/5 : déploiement des troupes")
            for feature in found_features:
                feature.bot.ActivateWindow()
                feature.DeployTroops()

            time.sleep(6)
            self.view.ShowText("Étape 4/5 : activation des héros")
            for feature in found_features:
                feature.bot.ActivateWindow()
                feature.ActivateHeroes()

            self.view.ShowText("Étape 5/5 : retour au village")
            for feature in found_features:
                feature.bot.ActivateWindow()
                feature.LeaveAttack()

            compteur += 1
            
    def RunProg(self):
        self.ConfigureBots()
        choix_bot = 100
        
        while(choix_bot != 9):
            self.view.Home()
            choix_bot = self.AskChoice()
            match choix_bot:
                case 1:
                    if(self.CallCheckWindow()):
                        if len(self.bots) == 1:
                            self.bots[0].FarmMDO()
                        else:
                            self.view.ShowText("Farm MDO multi-instance non disponible pour le moment.")
                case 2:
                    if(self.CallCheckWindow()):
                        self.RunFarmPrincipal()

                case 3:
                    if(self.CallCheckWindow()):
                        if len(self.bots) == 1:
                            self.bots[0].WallUPGRADE()
                        else:
                            self.view.ShowText("Wall Upgrade multi-instance non disponible pour le moment.")

                case 7:
                    if(self.CallCheckWindow()):
                        for bot in self.bots:
                            bot.ActivateWindow()
                            bot.SetZoom()

                case 8:
                    self.ConfigureBots()

                case 9:
                    print("Merci d'avoir utiliser le bot !")
                    print("A une prochaine !")