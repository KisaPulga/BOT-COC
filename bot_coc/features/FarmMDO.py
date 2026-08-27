import time
import pyautogui
import os
import random
from PIL import Image
import sys
import pygetwindow as gw

class FarmMDO:
    def __init__(self, bot):
        self.bot = bot
        # Image Charette elixir
        BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
        )

        self.image_charette = os.path.join(
            BASE_DIR,
            "images",
            "charette_elixir.png"
        )

        # Coordonnées boutons
        self.buttons = {}
        self.x_troups = []
        self.y_troups = None
        self.spawn_positions = []

        self.x_scroll_start = None
        self.y_scroll_start = None

        self.heros = False # a modifier si on a un héro

        self.tryFoundAttackMDO = 0

        self.purple_color = (198,55,254)
    
    def SetupPositions(self):
        # Boutons
        self.buttons = {
            "attack" : self.bot.ScaleXY(67, 542 - 38), # OK
            "find" : self.bot.ScaleXY(753, 415 - 38), # OK
            "surrender" : self.bot.ScaleXY(75, 437 - 38),# OK
            "surrender_okay" : self.bot.ScaleXY(617, 408 - 38),# OK
            "return_home" : self.bot.ScaleXY(510, 523 - 38),# OK
            "cancel" : self.bot.ScaleXY(509, 537 - 38),
            "elixir_cart_take" : self.bot.ScaleXY(750, 520 - 38),# OK
            "elixir_cart_leave" : self.bot.ScaleXY(852, 97 - 38),# OK
            "scroll_start" : self.bot.ScaleXY(721,184 - 38), # OK
            "scroll_end" : self.bot.ScaleXY(721,584 - 38),# OK
            "purple_troup" : self.bot.ScaleXY(213,513 - 38) # OK
        }
    
        x_troups_init = [102, 193, 275, 357, 435, 514, 597]# OK
        self.y_troups = self.bot.ScaleXY(0,553 - 38)[1]# OK
        self.x_troups = [self.bot.ScaleXY(x, 553 - 38)[0] for x in x_troups_init]

        troups_spawn_init = [
            (114,238 - 38),(150,349 - 38),(677,315 - 38),(146,215 - 38),# OK
            (128,298 - 38),(62,284 - 38),(74,284 - 38),(690,283 - 38), # OK
            (639,364 - 38),(242,74 - 38),(157,136 - 38),(113,311 - 38), # OK
            (695,349 - 38),(668,136 - 38) # OK
        ]
        self.spawn_positions = [
            self.bot.ScaleXY(x, y) for x, y in troups_spawn_init 
        ]

    def FindAttack(self):
        self.bot.Click(self.buttons["attack"])
        self.bot.Click(self.buttons["find"])

        start_wait = time.time()

        while not self.bot.VerifyPixel(self.buttons["purple_troup"], self.purple_color):
            time.sleep(1)
            print(pyautogui.pixel(int(self.buttons["purple_troup"][0]), int(self.buttons["purple_troup"][1])))
            if time.time() - start_wait > 20:
                return False  # pas trouvé
        return True  # trouvé

    def LeaveAttack(self):
        # Abandonne l'attaque et rentre
        self.bot.Click(self.buttons["surrender"])
        self.bot.Click(self.buttons["surrender_okay"])
        self.bot.Click(self.buttons["return_home"])


    def Attack(self):
        while True:
            success = self.FindAttack()

            if success:
                print("     Adversaire trouvé !")
                break  # On sort de la boucle

            print("     Bloqué en recherche → retour maison")
            self.tryFoundAttackMDO += 1
            if self.tryFoundAttackMDO >= 15:
                sys.exit()
            # Bouton retour maison (même position que attack1)
            self.bot.ClickFast(self.buttons["cancel"])
            time.sleep(2)  # Laisse le temps de revenir au village

        # Vérifie s'il y a au moins un héros, demandé au user au début
        base_troups = self.x_troups if self.heros else self.x_troups[:-1]
        put_troups = base_troups.copy() # créer une copie permet de pas modifier la liste de base
        random.shuffle(put_troups)

        # On boucle sur le nombre de troupe pour les placer
        for troup_x in put_troups:
            spawn = random.choice(self.spawn_positions)
            self.bot.Click((troup_x,self.y_troups))
            self.bot.Click(spawn)

        #Active les capacités des troupes
        ability_troups = self.x_troups if self.heros else self.x_troups[:-1]
        for troup_x in ability_troups:
            self.bot.Click((troup_x, self.y_troups))

        # Patiente un peu
        time.sleep(random.uniform(2, 4))
        self.LeaveAttack()


    def Scroll(self):
        # Scroll pour aller vers la charette à Elixir
        pyautogui.moveTo(self.buttons["scroll_start"][0],self.buttons["scroll_start"][1], self.bot.RandomClickTime(), pyautogui.easeInOutQuad)
        time.sleep(0.2)
        pyautogui.mouseDown(button='left')
        time.sleep(0.2)
        pyautogui.moveTo(self.buttons["scroll_end"][0],self.buttons["scroll_end"][1], self.bot.RandomClickTime(), pyautogui.easeInOutQuad)
        pyautogui.mouseUp(button='left')
    
    def FindElixir(self):
        try:
            # redimensionne l'image en fonction des x / y du user
            image = Image.open(self.image_charette)
            nouvelle_largeur = int(image.width * self.bot.x_ratio)
            nouvelle_hauteur = int(image.height * self.bot.y_ratio)
            image_resized = image.resize((nouvelle_largeur, nouvelle_hauteur))
                
            charette_x, charette_y = pyautogui.locateCenterOnScreen(image_resized, confidence=0.5)
            self.bot.Click((charette_x, charette_y))

            time.sleep(1)
                
            # Recupere l'elixir 
            self.bot.Click(self.buttons["elixir_cart_take"])
            self.bot.Click(self.buttons["elixir_cart_leave"])

            print("Elixir récupéré !")

        except pyautogui.ImageNotFoundException:
            print("Charette à élixir pas trouvé, peut être au prochain tour !")


    def RunFEAT(self):
        win = gw.getWindowsWithTitle("MuMu")[0]
        self.SetupPositions()

        win.activate()
        time.sleep(2)
        compteur = 1

        while(True):
            print("--------------------------------")
            for i in range(5):
                self.tryFoundAttackMDO = 0
                start_time = time.time()
                print(f"Séquence {compteur} :")
                print("     Début..")
                
                self.Attack()

                # Patiente un peu
                time.sleep(random.uniform(3, 4))

                # Calcule le temps et l'affiche
                end_time = time.time()
                temps = round(end_time - start_time, 2)
                print("     Fin, temps écoulé : " + str(temps) + "s")
                compteur += 1
                time.sleep(1)
            print("--------------------------------")
            
            self.Scroll()
            time.sleep(2)
            self.FindElixir()