########################
#   CLASS CONTROLLER   #
########################

from bot_coc.bot import Bot
import ctypes
import json
from pathlib import Path
import time

class Controller:
    def __init__(self, view):
        self.view = view
        self.bots = []
        self.coordinates_file = Path(__file__).resolve().parent.parent / "coordinates.json"
        self.pause_key_was_down = False

    def AskBotCount(self):
        while True:
            try:
                count = int(input("Combien d'instances souhaitez-vous lancer ? "))
                if count > 0:
                    return count
                print("Veuillez saisir un nombre supérieur à zéro.")
            except ValueError:
                print("Entrée invalide ! Veuillez saisir un chiffre.")

    def AskCoordinatesChoice(self):
        while True:
            choice = input("Utiliser les coordonnées précédemment enregistrées ? (o/n) ").strip().lower()
            if choice in ("o", "oui", "y", "yes"):
                return True
            if choice in ("n", "non", "no"):
                return False
            print("Entrée invalide ! Répondez par oui ou non.")

    def LoadCoordinates(self):
        if not self.coordinates_file.exists():
            return []

        try:
            with self.coordinates_file.open("r", encoding="utf-8") as file:
                coordinates = json.load(file)
        except (OSError, json.JSONDecodeError):
            self.view.ShowText("Impossible de lire coordinates.json. De nouvelles coordonnées seront demandées.")
            return []

        required_keys = {"x_left", "y_left", "x_right", "y_right"}
        if not isinstance(coordinates, list):
            return []
        return [
            item for item in coordinates
            if isinstance(item, dict) and required_keys.issubset(item)
        ]

    def SaveCoordinates(self, coordinates):
        with self.coordinates_file.open("w", encoding="utf-8") as file:
            json.dump(coordinates, file, indent=4)

    def ConfigureBots(self):
        count = self.AskBotCount()
        saved_coordinates = self.LoadCoordinates()
        use_saved = bool(saved_coordinates) and self.AskCoordinatesChoice()
        self.bots = []
        configured_coordinates = []

        for index in range(count):
            self.view.ShowText(f"\nParamétrage de l'instance {index + 1}/{count}")
            bot = Bot()
            if use_saved and index < len(saved_coordinates):
                coordinates = bot.SetUserCoordinates(saved_coordinates[index], self.CallView)
            else:
                coordinates = bot.DefineUserCoordinates(self.CallView)
            self.bots.append(bot)
            configured_coordinates.append(coordinates)

        self.SaveCoordinates(configured_coordinates)
        
    def AskChoice(self):
        while True:
            try:
                choix = int(input("Que souhaitez-vous faire ? "))
                return choix
            except ValueError:
                print("Entrée invalide ! Veuillez saisir un chiffre.")

    def CallView(self, message):
        self.view.ShowText(message)

    def PauseRequested(self):
        key_is_down = bool(ctypes.windll.user32.GetAsyncKeyState(ord("Q")) & 0x8000)
        if key_is_down and not self.pause_key_was_down:
            self.pause_key_was_down = True
            self.view.ShowText("Pause demandée : retour au menu...")
            return True
        if not key_is_down:
            self.pause_key_was_down = False
        return False

    def WaitWithPauseCheck(self, duration):
        end_time = time.time() + duration
        while time.time() < end_time:
            if self.PauseRequested():
                return True
            time.sleep(0.2)
        return False

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
        self.view.ShowText("Appuyez sur Q à tout moment pour mettre le farm en pause et revenir au menu.")
        for bot in self.bots:
            bot.farm_principal.pause_callback = self.PauseRequested

        while True:
            self.view.ShowText(f"\n===== Séquence {compteur} =====")
            features = [bot.farm_principal for bot in self.bots]

            self.view.ShowText("Étape 1/5 : lancement des attaques")
            for feature in features:
                if self.PauseRequested():
                    return
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
                if feature.pause_requested:
                    return

            self.view.ShowText("Étape 3/5 : déploiement des troupes")
            for feature in found_features:
                if self.PauseRequested():
                    return
                feature.bot.ActivateWindow()
                feature.DeployTroops()

            if self.WaitWithPauseCheck(6):
                return
            self.view.ShowText("Étape 4/5 : activation des héros")
            for feature in found_features:
                if self.PauseRequested():
                    return
                feature.bot.ActivateWindow()
                feature.ActivateHeroes()

            self.view.ShowText("Étape 5/5 : retour au village")
            for feature in found_features:
                if self.PauseRequested():
                    return
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
                            self.bots[0].farm_mdo.pause_callback = self.PauseRequested
                            self.view.ShowText("Appuyez sur Q pour mettre le Farm MDO en pause et revenir au menu.")
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