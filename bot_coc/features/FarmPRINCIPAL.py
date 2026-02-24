import time
import pyautogui
import os
import random
import pytesseract
from PIL import Image

class FarmPRINCIPAL:
    def __init__(self, bot):
        self.bot = bot
        # Coordonnées boutons
        self.buttons = {}
        self.x_troups = []
        self.y_troups = None
        self.spawn_positions = []

        # Nombre de héros dispo, et nombre de troupe d'evenement
        self.heros = 4
        self.troup_event = 1

    def SetupPositions(self):
        # Boutons
        self.buttons = {
            "attack1" : self.ScaleXY(50, 437),
            "find" : self.ScaleXY(121, 336),
            "attack2" : self.ScaleXY(735, 414),
            "surrender" : self.ScaleXY(51, 382),
            "surrender_okay" : self.ScaleXY(513, 301),
            "return_home" : self.ScaleXY(434, 415),
        }

        # enlever 2 valeur a self.x_troups si pas de troupe d'event
        x_troups_init = [155, 209, 270, 325, 377, 431, 494, 547]
        self.y_troups = self.ScaleXY(0,444)[1]
        self.x_troups = [self.ScaleXY(x, self.y_troups)[0] for x in x_troups_init]

        troups_spawn_init = [
            (728,85),(778,322),(817,165),(737,345),
            (834,200),(796,276),(666,368),(83,288),
            (140,102),(43,251),(30,188),(175,357),
            (253,19),(595,385)
        ]
        self.spawn_positions = [
            self.ScaleXY(x, y) for x, y in troups_spawn_init 
        ]

    def Attack(self):
        # Attaquer puis trouver un adversaire
        self.bot.Click(self.buttons["attack"])
        self.bot.Click(self.buttons["find"])

        # On attend de trouver un adversaire
        time.sleep(random.uniform(8, 10))

        


    def RunFEAT(self):
        self.bot.SetZoom()
