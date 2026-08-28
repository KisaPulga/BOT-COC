########################
#   CLASS CONTROLLER   #
########################

import ctypes
import json
from pathlib import Path
import time

class Controller:
    def __init__(self, view, bot):
        self.view = view
        self.bot = bot
        self.coordinates_file = Path(__file__).resolve().parent.parent / "coordinates.json"
        self.pause_key_was_down = False
        self.bot.farm_mdo.pause_callback = self.PauseRequested
        self.bot.farm_principal.pause_callback = self.PauseRequested

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
            return None

        try:
            with self.coordinates_file.open("r", encoding="utf-8") as file:
                coordinates = json.load(file)
        except (OSError, json.JSONDecodeError):
            self.view.ShowText("Impossible de lire coordinates.json. De nouvelles coordonnées seront demandées.")
            return None

        if isinstance(coordinates, dict):
            saved_coordinates = coordinates
        elif isinstance(coordinates, list) and coordinates:
            saved_coordinates = coordinates[0]
        else:
            return None

        required_keys = {"x_left", "y_left", "x_right", "y_right"}
        if required_keys.issubset(saved_coordinates):
            return saved_coordinates
        return None

    def SaveCoordinates(self, coordinates):
        with self.coordinates_file.open("w", encoding="utf-8") as file:
            json.dump(coordinates, file, indent=4)

    def ConfigureBot(self, force_new=False):
        saved_coordinates = self.LoadCoordinates()
        if saved_coordinates and not force_new and self.AskCoordinatesChoice():
            self.bot.SetUserCoordinates(saved_coordinates, self.CallView)
        else:
            coordinates = self.bot.DefineUserCoordinates(self.CallView)
            self.SaveCoordinates(coordinates)
        
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
        verif, text = self.bot.CheckWindow()
        if not verif:
            self.view.ShowText(text)
        return verif
            
    def RunProg(self):
        self.ConfigureBot()
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

                case 3:
                    if(self.CallCheckWindow()):
                        self.bot.WallUPGRADE()

                case 7:
                    if(self.CallCheckWindow()):
                        self.bot.SetZoom()

                case 8:
                    self.ConfigureBot(force_new=True)

                case 9:
                    print("Merci d'avoir utiliser le bot !")
                    print("A une prochaine !")