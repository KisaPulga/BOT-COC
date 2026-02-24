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
        self.spawn_troups_positions = []
        self.spawn_spell_positions = []

        # Nombre de héros manquant, et nombre de troupe d'evenement
        self.heros = 0
        self.troup_event = True

    def SetupPositions(self):
        # Boutons
        self.buttons = {
            "attack1" : self.bot.ScaleXY(50, 437),
            "find" : self.bot.ScaleXY(121, 336),
            "attack2" : self.bot.ScaleXY(735, 414),
            "surrender" : self.bot.ScaleXY(51, 382),
            "surrender_okay" : self.bot.ScaleXY(513, 301),
            "return_home" : self.bot.ScaleXY(434, 415),
        }

        # enlever 2 valeur a self.x_troups si pas de troupe d'event
        x_troups_init = [155, 209, 270, 325, 377, 431, 494, 547]
        self.y_troups = self.bot.ScaleXY(0,444)[1]
        self.x_troups = [self.bot.ScaleXY(x, self.y_troups)[0] for x in x_troups_init]

        troups_spawn_init = [
            (151,197),(202,157),(253,114),(309,76),(363,40),(410,7),(497,26),(543,58),(593,87),(651,127),(698,171)
        ]
        self.spawn_troups_positions = [
            self.bot.ScaleXY(x, y) for x, y in troups_spawn_init
        ]

        troups_spell_init = [
            (237,217),(330,147),(440,78),(522,122),(628,197)
        ]
        self.spawn_spell_positions= [
            self.bot.ScaleXY(x, y) for x, y in troups_spell_init 
        ]


    def FindAttack(self):
        self.bot.Click(self.buttons["attack1"])
        self.bot.Click(self.buttons["find"])
        self.bot.Click(self.buttons["attack2"])

    def LeaveAttack(self):
        # Abandonne l'attaque et rentre
        self.bot.Click(self.buttons["surrender"])
        self.bot.Click(self.buttons["surrender_okay"])
        self.bot.Click(self.buttons["return_home"])

    def Attack(self):
        self.FindAttack()

        # On attend de trouver un adversaire
        time.sleep(random.uniform(8, 10))

        base_troups = self.x_troups[:-self.heros] if self.heros > 0 else self.x_troups.copy()
        base_troups = base_troups if not self.troup_event else base_troups[:-1]

        if(self.troup_event):
            self.bot.Click((base_troups[0], self.y_troups))
            for spawn in self.spawn_troups_positions:
                self.bot.ClickFast(spawn)
                print(spawn)



    def RunFEAT(self):
        self.SetupPositions()

        time.sleep(2)
        self.Attack()
