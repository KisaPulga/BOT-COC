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
            "upgrade_gold" : self.bot.ScaleXY(432, 390),
            "upgrade_elixir" : self.bot.ScaleXY(502, 390),
            "upgrade" : self.bot.ScaleXY(610, 420),
        }
        self.pos_ressources = {
            "storage_gold" : self.bot.ScaleXY(721,20),
            "storage_elixir" : self.bot.ScaleXY(721,57),
        }
        self.random = self.bot.ScaleXY(822,200)
    
    def FindWall(self):
        hdv_x, hdv_y = None, None

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

            hdv_x,hdv_y = pyautogui.locateCenterOnScreen(image_resized14, confidence=0.8)
            if(hdv_x is None) :
                hdv_x,hdv_y = pyautogui.locateCenterOnScreen(image_resized15, confidence=0.8)
            if(hdv_x is None) :
                hdv_x,hdv_y = pyautogui.locateCenterOnScreen(image_resized16, confidence=0.8)

            if(hdv_x != None):

                return hdv_x, hdv_y
        
        except pyautogui.ImageNotFoundException:
            print("Pas trouve")


    def UpgradeWall(self):
        if(self.bot.VerifyPixel(self.pos_ressources["storage_gold"], self.gold_color)):
            pos = self.FindWall()
            if pos:
                x, y = pos
                self.bot.Click((x, y))
            time.sleep(0.3)
            self.bot.Click(self.buttons["upgrade_gold"])
            time.sleep(0.3)
            self.bot.Click(self.buttons["upgrade"])
            self.walls +=1

        if(self.bot.VerifyPixel(self.pos_ressources["storage_elixir"], self.elixir_color, 0.20)):
            pos = self.FindWall()
            if pos:
                x, y = pos
                self.bot.Click((x, y))
            time.sleep(0.3)
            self.bot.Click(self.buttons["upgrade_elixir"])
            time.sleep(0.3)
            self.bot.Click(self.buttons["upgrade"])
            self.walls +=1
        

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
            print(pyautogui.pixel(int(self.pos_ressources["storage_elixir"][0]),int(self.pos_ressources["storage_elixir"][1])))
            print(self.elixir_color)
            self.UpgradeWall()
            print(f"Murs amélioré sur cette session : {self.walls} !")
            end_time = time.time()
            temps = round(end_time - start_time, 2)
            print("     Fin, temps écoulé : " + str(temps) + "s")
            compteur += 1
            print("--------------------------------")
            time.sleep(2)

