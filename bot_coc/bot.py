#################
#   CLASS BOT   #
#################
  
import time
import pyautogui
import random
import pygetwindow as gw
import ctypes
from bot_coc.features.FarmMDO import FarmMDO
from bot_coc.features.FarmPRINCIPAL import FarmPRINCIPAL
from bot_coc.features.WallUPGRADE import WallUPGRADE

class Bot():
    def __init__(self):

        # Longueurs initiales
        self.x_width_init = 1017
        self.y_height_init = 612 - 38

        # Valeurs de l'utilisateurs
        self.x_width_user = None
        self.y_height_user = None
        self.x_left_user = None
        self.y_left_user = None
        self.window = None
        self.window_title = None


        # On initialise un objet par feature
        self.farm_mdo = FarmMDO(self)
        self.farm_principal = FarmPRINCIPAL(self)
        self.wall_upgrade = WallUPGRADE(self, self.farm_principal)

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
        x_left_user, y_left_user = pyautogui.position()
        callbackView(f"Top Left : {x_left_user}, {y_left_user}")

        callbackView("Place la souris en bas à droite puis appuie sur ENTER")
        input()
        x_right_user, y_right_user = pyautogui.position()
        callbackView(f"Bottom Right : {x_right_user}, {y_right_user}")

        coordinates = {
            "x_left": x_left_user,
            "y_left": y_left_user,
            "x_right": x_right_user,
            "y_right": y_right_user,
        }
        self.SetUserCoordinates(coordinates, callbackView)
        return coordinates

    def SetUserCoordinates(self, coordinates, callbackView):
        self.x_left_user = coordinates["x_left"]
        self.y_left_user = coordinates["y_left"]
        self.x_width_user = coordinates["x_right"] - self.x_left_user
        self.y_height_user = coordinates["y_right"] - self.y_left_user

        center_x = int(self.x_left_user + self.x_width_user / 2)
        center_y = int(self.y_left_user + self.y_height_user / 2)
        windows = gw.getWindowsAt(center_x, center_y)
        if windows:
            self.window = windows[0]
            self.window_title = self.window.title
            callbackView(f"Fenêtre associée : {self.window.title}")
        else:
            callbackView("Fenêtre introuvable dans cette zone.")

        callbackView("")
        callbackView("Paramétrage terminé, vous pouvez maintenant utiliser le bot !")
        return coordinates

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

        return int(new_x), int(new_y)
    
    def CheckWindow(self):
        if self.x_width_user is None or self.y_height_user is None:
            return False, "Avant d'utiliser le bot, vous devez le paramétrer."
        elif self.window is None:
            return False, "Aucune fenêtre n'est associée à ce bot."
        else:
            return True, "Ok"

    def ActivateWindow(self):
        if self.window is None:
            raise RuntimeError("Aucune fenêtre n'est associée à ce bot.")

        if not ctypes.windll.user32.IsWindow(self.window._hWnd):
            center_x = int(self.x_left_user + self.x_width_user / 2)
            center_y = int(self.y_left_user + self.y_height_user / 2)
            windows = gw.getWindowsAt(center_x, center_y)
            matching_windows = [
                window for window in windows
                if window.title == self.window_title
            ]
            if not matching_windows:
                raise RuntimeError(
                    f"La fenêtre associée '{self.window_title}' est introuvable."
                )
            self.window = matching_windows[0]

        try:
            if self.window.isMinimized:
                self.window.restore()
            self.window.activate()
        except Exception:
            center_x = int(self.x_left_user + self.x_width_user / 2)
            center_y = int(self.y_left_user + self.y_height_user / 2)
            windows = [
                window for window in gw.getWindowsAt(center_x, center_y)
                if window.title == self.window_title
            ]
            if not windows:
                raise RuntimeError(
                    f"Impossible de réactiver la fenêtre '{self.window_title}'."
                )
            self.window = windows[0]
            self.window.activate()
        time.sleep(0.3)
        
    def FindMiddle(self):
        pyautogui.moveTo((self.x_left_user + (self.x_width_user / 2)), (self.y_left_user + (self.y_height_user / 2)),  self.RandomClickTime(), pyautogui.easeInOutQuad)

    def SetZoom(self):
        self.FindMiddle()
        for i in range(25):
            pyautogui.scroll(1000)
        for i in range(16):
            pyautogui.scroll(-1000)

    def VerifyPixel(self, position, color, tolerance=0.3):
        x = int(position[0])
        y = int(position[1])
        
        pixel = pyautogui.pixel(x, y)
        
        for i in range(3):  # R, G, B
            min_val = int(color[i] * (1 - tolerance))
            max_val = int(color[i] * (1 + tolerance))
            
            if not (min_val <= pixel[i] <= max_val):
                return False
        return True
    
    def FarmMDO(self):
        self.farm_mdo.RunFEAT()

    def FarmPRINCIPAL(self):
        self.farm_principal.RunFEAT()

    def FarmPRINCIPALCycle(self):
        self.farm_principal.RunCycle()

    def WallUPGRADE(self):
        self.wall_upgrade.RunFEAT()
        