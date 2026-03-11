import time
import pyautogui
import os
import random
import pytesseract
from PIL import Image

class WallUPGRADE:
    def __init__(self, bot, farm):
        # bots
        self.farm_principal = farm
        self.bot = bot
        # Images
        BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
        )

        self.image_wall14 = os.path.join(
            BASE_DIR,
            "images",
            "wall14.png"
        )
        self.image_wall15 = os.path.join(
            BASE_DIR,
            "images",
            "wall15.png"
        )
        self.image_wall16 = os.path.join(
            BASE_DIR,
            "images",
            "wall16.png"
        )

        # coordonnées btn
        self.buttons = {}
        self.pos_ressources = {}
        self.gold_color = (213,195,100)
        self.elixir_color = (222,143,222)
        self.walls = 0
        self.random = None
    
    def SetupPositions(self):
        self.buttons = {
            "upgrade_gold" : self.bot.ScaleXY(467, 390),
            "upgrade_elixir" : self.bot.ScaleXY(541, 390),
            "upgrade" : self.bot.ScaleXY(610, 420),
        }
        self.pos_ressources = {
            "storage_gold" : self.bot.ScaleXY(721,20),
            "storage_elixir" : self.bot.ScaleXY(721,57),
        }
        self.random = self.bot.ScaleXY(822,200)
    
    def FindWall(self):
        position= None

        try:
            image14 = Image.open(self.image_wall14)
            nouvelle_largeur14 = int(image14.width * self.bot.x_ratio)
            nouvelle_hauteur14 = int(image14.height * self.bot.y_ratio)
            image_resized14 = image14.resize((nouvelle_largeur14, nouvelle_hauteur14))

            image15 = Image.open(self.image_wall15)
            nouvelle_largeur15 = int(image15.width * self.bot.x_ratio)
            nouvelle_hauteur15 = int(image15.height * self.bot.y_ratio)
            image_resized15 = image15.resize((nouvelle_largeur15, nouvelle_hauteur15))

            image16 = Image.open(self.image_wall16)
            nouvelle_largeur16 = int(image16.width * self.bot.x_ratio)
            nouvelle_hauteur16 = int(image16.height * self.bot.y_ratio)
            image_resized16 = image16.resize((nouvelle_largeur16, nouvelle_hauteur16))

            position = pyautogui.locateCenterOnScreen(image_resized14, confidence=0.8, region=(self.bot.x_left_user, self.bot.y_left_user, self.bot.x_width_user, self.bot.y_height_user))
            if(position is None) :
                print("pas de mur 14 trouvé")
                position = pyautogui.locateCenterOnScreen(image_resized15, confidence=0.8, region=(self.bot.x_left_user, self.bot.y_left_user, self.bot.x_width_user, self.bot.y_height_user))
            if(position is None) :
                print("pas de mur 15 trouvé")
                position = pyautogui.locateCenterOnScreen(image_resized16, confidence=0.8, region=(self.bot.x_left_user, self.bot.y_left_user, self.bot.x_width_user, self.bot.y_height_user))

            if(position != None):
                return position
            else:
                print("PAS DE MUR 16 trouvé")
                return None
        
        except pyautogui.ImageNotFoundException:
            print("Pas trouve")


    def UpgradeWall(self):
        if(self.bot.VerifyPixel(self.pos_ressources["storage_gold"], self.gold_color)):
            print("OR PLEIN")
            for i in range(1):
                pos = self.FindWall()
                if pos:
                    self.bot.Click(pos)
                    print("         CLICK SUR UN MUR AVEC OR")
                    time.sleep(2)
                    self.bot.Click(self.buttons["upgrade_gold"])
                    print("         CLICK BOUTON AMELIORER MUR AVEC OR")
                    time.sleep(1)
                    self.bot.Click(self.buttons["upgrade"])
                    print("         CLICK SUR BOUTON AMELIORER AVEC OR")
                    time.sleep(1)
                    self.bot.Click(self.random)
                    print("         CLICK A COTE POUR ENLEVER LE MENU AVEC OR")
                    time.sleep(1)
                    print("     Amélioration à l'or !")
                    self.walls +=1
        else:
            print("         Pas assez d'or")

        if(self.bot.VerifyPixel(self.pos_ressources["storage_elixir"], self.elixir_color, 0.20)):
            print("ELIXIR PLEIN")
            for i in range(1):
                pos = self.FindWall()
                if pos:
                    self.bot.Click(pos)
                    print("         CLICK SUR UN MUR AVEC ELIXIR")
                    time.sleep(2)
                    self.bot.Click(self.buttons["upgrade_elixir"])
                    print("         CLICK BOUTON AMELIORER MUR AVEC ELIXIR")
                    time.sleep(1)
                    self.bot.Click(self.buttons["upgrade"])
                    print("         CLICK SUR BOUTON AMELIORER AVEC ELIXIR")
                    time.sleep(1)
                    self.bot.Click(self.random)
                    print("         CLICK A COTE POUR ENLEVER LE MENU AVEC ELIXIR")
                    time.sleep(1)
                    print("     Amélioration à l'élixir !")
                    self.walls +=1
        else:
            print("         Pas assez d'elixir")
        

    def RunFEAT(self):
        self.SetupPositions()
        self.farm_principal.SetupPositions()

        compteur = 1
        print("--------------------------------")
        while(True):
            start_time = time.time()
            print(f"Séquence {compteur} :")
            print("     Début..")

            self.farm_principal.Attack()

            time.sleep(3)

            print("     Vérification ressources..")
            self.UpgradeWall()

            print(f"     Murs amélioré sur cette session : {self.walls} !")
            end_time = time.time()
            temps = round(end_time - start_time, 2)
            print("     Fin, temps écoulé : " + str(temps) + "s")
            compteur += 1
            print("--------------------------------")
            time.sleep(2)

