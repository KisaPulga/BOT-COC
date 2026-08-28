import time
import random
import sys
import pygetwindow as gw

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
        self.troup_event = False

        self.tryFoundAttackPRINCIPAL = 0

        self.red_verif_attack_color = (208,13,14)
        self.grey_star_color = (174,175,170)
        self.orange_verif_home_color = (229,151,57)
        self.positions_ready = False


    def SetupPositions(self):
        # Boutons
        self.buttons = {
            "attack1" : self.bot.ScaleXY(67,541 - 38), # OK
            "find" : self.bot.ScaleXY(175,461 - 38), # OK
            "attack2" : self.bot.ScaleXY(904,549 - 38),  # OK
            "surrender" : self.bot.ScaleXY(75,467 - 38), # OK
            "verif_attack" : self.bot.ScaleXY(105,480 - 38), # OK
            "surrender_okay" : self.bot.ScaleXY(624,409 - 38), # OK
            "return_home" : self.bot.ScaleXY(510,530 - 38),  # OK
            "one_star" : self.bot.ScaleXY(864,470 - 38),  # OK
            "verif_home" : self.bot.ScaleXY(106,524 - 38) # OK
        }

        # enlever 2 valeur a self.x_troups si pas de troupe d'event
        x_troups_init = [113, 190, 273, 351, 430, 507, 586, 663]  # OK
        self.y_troups = self.bot.ScaleXY(0,562 - 38)[1]  # OK
        self.x_troups = [self.bot.ScaleXY(x, self.y_troups)[0] for x in x_troups_init]

        troups_spawn_init_1 = [
            (135,294),(176,245),(235,209),(295,154),(352,120),(462,60),(336,129),(414,92),(223,232),(288,172),(281,170),(338,133),(406,81),(440,64),(166,269),(387,106),(309,151)
        ]
        self.spawn_troups_positions_1  = [
            self.bot.ScaleXY(x, y - 38) for x, y in troups_spawn_init_1 
        ]

        troups_spell_init_1  = [
            (284,303),(392,214),(481,148),(396,329),(495,228)
        ]
        self.spawn_spell_positions_1 = [
            self.bot.ScaleXY(x, y - 38) for x, y in troups_spell_init_1  
        ]

        troups_spawn_init_2 = [
            (546,55),(586,86 ),(643,122),(683,149),(724,182),(763,211),(788,229),(816,253),(838,269),(692,159),(651,125),(599,83),(746,201),(698,161),(660,128),(805,236),(575,66)
        ]
        self.spawn_troups_positions_2  = [
            self.bot.ScaleXY(x, y - 38) for x, y in troups_spawn_init_2 
        ]

        troups_spell_init_2  = [
            (509,109),(612,200),(713,277),(494,190),(640,295)
        ]
        self.spawn_spell_positions_2 = [
            self.bot.ScaleXY(x, y - 38) for x, y in troups_spell_init_2  
        ]


    def StartAttackSearch(self):
        actions = [
            (self.bot.Click, (self.buttons["attack1"],)),
            (self.bot.Click, (self.buttons["find"],)),
            (self.bot.Click, (self.buttons["attack2"],)),
        ]
        self.ExecuteActions(actions)

    def WaitForAttack(self, timeout=20):
        start_wait = time.time()

        # verification du bouton rouge
        while not self.bot.VerifyPixel(self.buttons["verif_attack"],self.red_verif_attack_color):
            time.sleep(1)

            if time.time() - start_wait > timeout:
                return False  # pas trouvé

        return True  # trouvé

    def FindAttack(self):
        self.StartAttackSearch()
        return self.WaitForAttack()

    def CancelAttackSearch(self):
        self.bot.ClickFast(self.buttons["attack1"])

    @staticmethod
    def ExecuteActions(actions):
        for action, args in actions:
            action(*args)


    def LeaveAttack(self):
        # attente d'une etoile
        start_wait = time.time()
        while not self.bot.VerifyPixel(self.buttons["one_star"],self.grey_star_color):
            time.sleep(2)
            if time.time() - start_wait > 40:
                break

        # Abandonne l'attaque et rentre
        self.bot.Click(self.buttons["surrender"])
        time.sleep(0.2)
        self.bot.Click(self.buttons["surrender_okay"])
        time.sleep(0.2)
        self.bot.Click(self.buttons["return_home"])

        # attente d'etre a la base
        start_wait = time.time()
        while not self.bot.VerifyPixel(self.buttons["verif_home"],self.orange_verif_home_color):
            time.sleep(3)
            if time.time() - start_wait > 7:
                break



    def DeployTroops(self):
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

        actions = []

        # Spawn electro drag
        actions.append((self.bot.ClickFast, ((x_trp_edrag, self.y_troups),)))
        for spawn_edrag in spawn_troups_positions :
            actions.append((self.bot.ClickFast, (spawn_edrag,)))

        # Spawn troupe evenement
        if(x_trp_event):
            actions.append((self.bot.ClickFast, ((x_trp_event, self.y_troups),)))
            for spawn_event in spawn_troups_positions :
                actions.append((self.bot.ClickFast, (spawn_event,)))

        # Spawn héros - on met un héro 1 position sur 2
        for i, x_hero in enumerate(x_heroes):
            i *= 2
            actions.append((self.bot.ClickFast, ((x_hero, self.y_troups),)))
            actions.append((self.bot.ClickFast, (spawn_troups_positions[i],)))

        # Spawn spell
        actions.append((self.bot.ClickFast, ((x_spell, self.y_troups),)))
        for spawn_spell in spawn_spell_positions:
            actions.append((self.bot.ClickFast, (spawn_spell,)))

        self.ExecuteActions(actions)

    def ActivateHeroes(self):
        units = self.x_troups.copy()
        index = 1 + (1 if self.troup_event else 0)
        nbr_heros = 4 - self.heros
        x_heroes = units[index:index + nbr_heros]
        for capa_hero in x_heroes:
            self.bot.Click((capa_hero, self.y_troups))

    def Attack(self):
        while True:
            if self.FindAttack():
                print("     Adversaire trouvé !")
                break
            print("     Bloqué en recherche → retour maison")
            self.tryFoundAttackPRINCIPAL += 1
            if self.tryFoundAttackPRINCIPAL >= 15:
                sys.exit()
            self.CancelAttackSearch()
            time.sleep(2)

        self.DeployTroops()
        time.sleep(6)
        self.ActivateHeroes()
        self.LeaveAttack()


    def RunCycle(self):
        self.bot.ActivateWindow()
        if not self.positions_ready:
            self.SetupPositions()
            self.positions_ready = True

        start_time = time.time()
        self.tryFoundAttackPRINCIPAL = 0
        self.Attack()
        end_time = time.time()
        temps = round(end_time - start_time, 2)
        print("     Fin, temps écoulé : " + str(temps) + "s")

    def RunFEAT(self):
        compteur = 1
        print("--------------------------------")
        while(True):
            print(f"Séquence {compteur} :")
            print("     Début..")
            self.RunCycle()
            compteur += 1
            print("--------------------------------")
            time.sleep(5)
