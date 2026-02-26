#################
#   CLASS BOT   #
#################
  
import time
import pyautogui
import random
from bot_coc.features.FarmMDO import FarmMDO
from bot_coc.features.FarmPRINCIPAL import FarmPRINCIPAL

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
        self.farm_principal = FarmPRINCIPAL(self)

    @staticmethod
    def RandomClickTime():
        return random.uniform(0.4, 0.6)
    
    @staticmethod
    def RandomWaitTime():
        return random.uniform(0.9, 1.3)
    
    @property
    def x_ratio(self):
        return self.x_width_user / self.x_width_init

    @property
    def y_ratio(self):
        return self.y_height_user / self.y_height_init

    def DefineUserCoordinates(self, callbackView):
        
        callbackView("Place la souris en haut à gauche puis appuie sur ENTER")
        input()
        self.x_left_user, self.y_left_user = pyautogui.position()
        callbackView(f"Top Left : {self.x_left_user}, {self.y_left_user}")

        callbackView("Place la souris en bas à droite puis appuie sur ENTER")
        input()
        x_right_user, y_right_user = pyautogui.position()
        callbackView(f"Bottom Right : {x_right_user}, {y_right_user}")

        self.x_width_user = x_right_user - self.x_left_user
        self.y_height_user = y_right_user - self.y_left_user

        callbackView("")
        callbackView("Paramétrage terminé, vous pouvez maintenant utiliser le bot !")

        # self.x_left_user = -1172
        # self.y_left_user = 79
        # x_right_user = -293
        # y_right_user = 574
        # self.x_width_user = x_right_user - self.x_left_user
        # self.y_height_user = y_right_user - self.y_left_user

    def Click(self, position):
        pyautogui.moveTo(position[0], position[1],  self.RandomClickTime(), pyautogui.easeInOutQuad)
        pyautogui.click()
    
    def ClickFast(self, position):
        pyautogui.moveTo(position[0], position[1],  0.1, pyautogui.easeInOutQuad)
        time.sleep(0.1)
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
        
    def FindMiddle(self):
        pyautogui.moveTo((self.x_left_user + (self.x_width_user / 2)), (self.y_left_user + (self.y_height_user / 2)),  self.RandomClickTime(), pyautogui.easeInOutQuad)

    def SetZoom(self):
        self.FindMiddle()
        for i in range(25):
            pyautogui.scroll(1000)
        for i in range(16):
            pyautogui.scroll(-1000)

    def VerifyPixel(self, position, color):
        verif_color = pyautogui.pixel(position[0], position[1])
        if(verif_color == color):
            return True
        else:
            return False
    
    def FarmMDO(self):
        self.farm_mdo.RunFEAT()

    def FarmPRINCIPAL(self):
        self.farm_principal.RunFEAT()
        