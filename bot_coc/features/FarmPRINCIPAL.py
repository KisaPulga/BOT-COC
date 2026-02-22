from ..bot import Bot

class FarmPRINCIPAL(Bot):
    def __init__(self):
        # Coordonnées boutons
        self.buttons = {}
        self.x_troups = []
        self.y_troups = None
        self.spawn_positions = []

        self.heros = 4

    def SetupPositions(self):
        # Boutons
        self.buttons = {
            "attack1" : self.ScaleXY(50, 437),
            "find" : self.ScaleXY(121, 336),
            "attack2" : self.ScaleXY(735, 414),
            "surrender" : self.ScaleXY(52, 363),
            "surrender_okay" : self.ScaleXY(511, 300),
            "return_home" : self.ScaleXY(432, 409),
            "elixir_cart_take" : self.ScaleXY(638, 407),
            "elixir_cart_leave" : self.ScaleXY(725, 49),
            "scroll_start" : self.ScaleXY(700,262), 
            "scroll_end" : self.ScaleXY(700,462)
        }
    
        x_troups_init = [147, 213, 268, 326, 382, 439, 495]
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

