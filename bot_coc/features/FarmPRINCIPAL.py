import time
import random

class FarmPRINCIPAL:
    def __init__(self, bot):
        self.bot = bot
        # Coordonnées boutons
        self.buttons = {}
        self.x_troups = []
        self.y_troups = None
        self.spawn_troups_positions_1 = []
        self.spawn_spell_positions_1 = []
        self.spawn_troups_positions_2  = []
        self.spawn_spell_positions_2 = []

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

        troups_spawn_init_1 = [
            (150,172),(185,143),(232,109),(289,72),(332,35),(358,18),(297,41),(234,88),(160,145),(211,141),(249,75),(151,190),(155,151),(254,100),(116,208),(343,15),(299,45)
        ]
        self.spawn_troups_positions_1  = [
            self.bot.ScaleXY(x, y) for x, y in troups_spawn_init_1 
        ]

        troups_spell_init_1  = [
            (221,194),(328,132),(418,72),(315,229),(444,132),(417,231)
        ]
        self.spawn_spell_positions_1 = [
            self.bot.ScaleXY(x, y) for x, y in troups_spell_init_1  
        ]

        troups_spawn_init_2 = [
            (493,18),(530,44),(558,64),(584,81),(615,101),(640,119),(663,136),(687,155),(720,174),(748,197),(702,161),(647,118),(609,91),(573,60),(534,43),(582,80),(665,137)
        ]
        self.spawn_troups_positions_2  = [
            self.bot.ScaleXY(x, y) for x, y in troups_spawn_init_2 
        ]

        troups_spell_init_2  = [
            (472,106),(554,160),(633,219),(427,157),(518,233),(434,216)
        ]
        self.spawn_spell_positions_2 = [
            self.bot.ScaleXY(x, y) for x, y in troups_spell_init_2  
        ]


    def FindAttack(self):
        self.bot.Click(self.buttons["attack1"])
        time.sleep(0.2)
        self.bot.Click(self.buttons["find"])
        time.sleep(0.2)
        self.bot.Click(self.buttons["attack2"])
        
        # On attend de trouver un adversaire
        start_wait = time.time()
        while not (self.bot.VerifyPixel(self.bot.ScaleXY(64,390),(211,13,13))):
            time.sleep(2)
            if time.time() - start_wait > 15:
                print("Temps d'attente trop longue, on relance")
                self.LeaveInfinityLoop()

    def LeaveAttack(self):
        start_wait = time.time()
        while not self.bot.VerifyPixel(self.bot.ScaleXY(757,384),(174,175,170)):
            time.sleep(2)
            if time.time() - start_wait > 40:
                break

        # Abandonne l'attaque et rentre
        self.bot.Click(self.buttons["surrender"])
        time.sleep(0.2)
        self.bot.Click(self.buttons["surrender_okay"])
        time.sleep(0.2)
        self.bot.Click(self.buttons["return_home"])

    def LeaveInfinityLoop(self):
        self.bot.ClickFast(self.buttons["attack1"])
        time.sleep(1)
        self.FindAttack()


    def Attack(self):
        self.FindAttack()

        units = self.x_troups.copy()
        index = 0

        # Position X troupe evenement
        x_trp_event = None
        if(self.troup_event):
            x_trp_event = units[index]
            index += 1
        
        # Position X electro drag
        x_trp_edrag = units[index]
        index +=1

        # Positions X de chaque héros
        nbr_heros = 4 - self.heros
        x_heroes = units[index:index+nbr_heros]
        index += nbr_heros

        # Position X sorts
        x_spell = units[index]

        # choix coté attaque
        side = random.choice([1, 2])

        if side == 1:
            spawn_troups_positions = self.spawn_troups_positions_1
            spawn_spell_positions = self.spawn_spell_positions_1
        else:
            spawn_troups_positions = self.spawn_troups_positions_2
            spawn_spell_positions = self.spawn_spell_positions_2

        # Spawn electro drag
        self.bot.ClickFast((x_trp_edrag, self.y_troups))
        for spawn_edrag in spawn_troups_positions :
                self.bot.ClickFast(spawn_edrag)

        # Spawn troupe evenement
        if(x_trp_event):
            self.bot.ClickFast((x_trp_event, self.y_troups))
            for spawn_event in spawn_troups_positions :
                self.bot.ClickFast(spawn_event)

        # Spawn héros - on met un héro 1 position sur 2
        for i, x_hero in enumerate(x_heroes):
            i *= 2
            self.bot.ClickFast((x_hero, self.y_troups))
            self.bot.ClickFast((spawn_troups_positions[i]))

        # Spawn spell
        self.bot.ClickFast((x_spell, self.y_troups))
        for spawn_spell in spawn_spell_positions:
            self.bot.ClickFast((spawn_spell))

        # Activer capacité héros
        time.sleep(6)
        for capa_hero in x_heroes:
            self.bot.Click((capa_hero, self.y_troups))

        self.LeaveAttack()


    def RunFEAT(self):
        self.SetupPositions()
        compteur = 1
        

        time.sleep(2)
        print("--------------------------------")
        while(True):
            start_time = time.time()
            print(f"Séquence {compteur} :")
            print("     Début..")


            self.Attack()


            end_time = time.time()
            temps = round(end_time - start_time, 2)
            print("     Fin, temps écoulé : " + str(temps) + "s")
            compteur += 1
            print("--------------------------------")
            time.sleep(6)
