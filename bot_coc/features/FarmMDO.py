import time
import pyautogui
import os
import random
from PIL import Image

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
    
    def SetupPositions(self):
        # Boutons
        self.buttons = {
            "attack" : self.bot.ScaleXY(50, 437),
            "find" : self.bot.ScaleXY(642, 322),
            "surrender" : self.bot.ScaleXY(52, 363),
            "surrender_okay" : self.bot.ScaleXY(511, 300),
            "return_home" : self.bot.ScaleXY(432, 409),
            "elixir_cart_take" : self.bot.ScaleXY(638, 407),
            "elixir_cart_leave" : self.bot.ScaleXY(725, 49),
            "scroll_start" : self.bot.ScaleXY(700,262), 
            "scroll_end" : self.bot.ScaleXY(700,462)
        }
    
        x_troups_init = [147, 213, 268, 326, 382, 439, 495]
        self.y_troups = self.bot.ScaleXY(0,444)[1]
        self.x_troups = [self.bot.ScaleXY(x, self.y_troups)[0] for x in x_troups_init]

        troups_spawn_init = [
            (728,85),(778,322),(817,165),(737,345),
            (834,200),(796,276),(666,368),(83,288),
            (140,102),(43,251),(30,188),(175,357),
            (253,19),(595,385)
        ]
        self.spawn_positions = [
            self.bot.ScaleXY(x, y) for x, y in troups_spawn_init 
        ]

    def FindAttack(self):
        self.bot.Click(self.buttons["attack"])
        self.bot.Click(self.buttons["find"])

    def LeaveAttack(self):
        # Abandonne l'attaque et rentre
        self.bot.Click(self.buttons["surrender"])
        self.bot.Click(self.buttons["surrender_okay"])
        self.bot.Click(self.buttons["return_home"])


    def Attack(self):
        # Attaquer puis trouver un adversaire
        self.FindAttack()

        # On attend de trouver un adversaire
        while not (self.bot.VerifyPixel(self.bot.ScaleXY(224,415),(198,52,255))):
            time.sleep(2)

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

        self.SetupPositions()


        time.sleep(2)
        compteur = 1

        while(True):
            print("--------------------------------")
            for i in range(5):
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
            self.FindElixir()