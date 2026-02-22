#################
#   CLASS BOT   #
#################

import time
import pyautogui
import random

class Bot():
    def __init__(self, farmMDO):
        self.farm_mdo = farmMDO

        # Longueurs initiales
        self.x_width_init = 865
        self.y_height_init = 484

        # Valeurs de l'utilisateurs
        self.x_width_user = None
        self.y_height_user = None
        self.x_left_user = None
        self.y_left_user = None

    @staticmethod
    def RandomClickTime():
        return random.uniform(0.4, 0.6)
    
    @staticmethod
    def RandomWaitTime():
        return random.uniform(0.9, 1.3)

    def DefineUserCoordinates(self):
        print("Mettez la souris en haut a gauche de la fenetre")
        time.sleep(3)
        self.x_left_user, self.y_left_user = pyautogui.position()
        print("Mettez la souris en bas a droite de la fenetre")
        time.sleep(3)
        x_right_user, y_right_user = pyautogui.position()

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
    
    def FarmMDO(self):
        self.farm_mdo.RunFarmMDO()
        