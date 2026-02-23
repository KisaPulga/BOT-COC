#################
#   CLASS BOT   #
#################

import time
import pyautogui
import random
from bot_coc.features.FarmMDO import FarmMDO

class Bot():
    def __init__(self):

        # Longueurs initiales
        self.x_width_init = 865
        self.y_height_init = 484

        # Valeurs de l'utilisateurs
        self.x_width_user = None
        self.y_height_user = None
        self.x_left_user = None
        self.y_left_user = None


        # On initialise un objet par feature
        self.farm_mdo = FarmMDO(self)

    @staticmethod
    def RandomClickTime():
        return random.uniform(0.4, 0.6)
    
    @staticmethod
    def RandomWaitTime():
        return random.uniform(0.9, 1.3)
    
    @property
    def x_ratio(self):
        return self.x_width_user / self.x_width_init

    def DefineUserCoordinates(self, log_callback):
        
        log_callback("Place la souris en haut à gauche puis appuie sur ENTER")
        input()
        self.x_left_user, self.y_left_user = pyautogui.position()
        log_callback(f"Top Left : {self.x_left_user}, {self.y_left_user}")

        log_callback("Place la souris en bas à droite puis appuie sur ENTER")
        input()
        x_right_user, y_right_user = pyautogui.position()
        log_callback(f"Bottom Right : {x_right_user}, {y_right_user}")

        self.x_width_user = x_right_user - self.x_left_user
        self.y_height_user = y_right_user - self.y_left_user

    
    def Click(self, position):
        pyautogui.moveTo(position[0], position[1],  self.RandomClickTime(), pyautogui.easeInOutQuad)
        pyautogui.click()
    
    def ScaleXY(self, x_base, y_base):
        x_ratio_btn = x_base / self.x_width_init
        y_ratio_btn = y_base / self.y_height_init

        new_x = self.x_left_user + x_ratio_btn * self.x_width_user
        new_y = self.y_left_user + y_ratio_btn * self.y_height_user

        return new_x,new_y
    
    def CheckWindow(self):
        if self.x_width_user is None or self.y_height_user is None:
            return False, "Avant d'utiliser le bot, vous devez le paramétrer."
        else:
            return True, "Ok"
    
    def FarmMDO(self):
        self.farm_mdo.RunFarmMDO()
        