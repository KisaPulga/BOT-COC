import pyautogui

while(True):
    position = pyautogui.position()
    r,g,b = pyautogui.pixel(position.x, position.y)
    print(position, ' ' , (r,g,b))