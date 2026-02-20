import time
import pyautogui
import os
import random
import pytesseract

# Lien vers pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#############
# VARIABLES #
#############

# Boutons
btn_attaquer = (50, 475)
btn_trouver = (642, 360)
btn_capituler = (52, 401)
btn_capituler_ok = (511, 338)
btn_rentrer = (432, 447)
btn_recuperer_charette = (638, 445)
btn_quitter_charette = (725, 87)

# Troupes
x_trp = [147, 213, 268, 326, 382, 439, 495]
y_trp = 482
x_trp_spawn = [728,778,817,737,834,796,666,83,140,43,30,175,253,595]
y_trp_spawn = [123,360,203,383,238,314,406,326,140,289,226,395,57,423]
heros = False # a modifier si on a un héro

# Charette elixir
image_charette = os.path.join(os.path.dirname(__file__), 'images/charette_elixir.png')

#############
# FONCTIONS #
#############

def RandomTrpClic(liste):
    copie = liste.copy()
    random.shuffle(copie)
    return copie

def RandomTrpSpawn():
    return random.randint(0,13)

def RandomTimeClic():
    return random.uniform(0.4, 0.6)

def RandomTimeWait():
    return random.uniform(0.9, 1.3)


time.sleep(2)
compteur = 1

while(True):
    print("--------------------------------")
    for i in range(5):
        start_time = time.time()
        print(f"Séquence {compteur} :")
        print("     Début..")
        # Attaquer puis trouver un adversaire
        pyautogui.moveTo(btn_attaquer[0], btn_attaquer[1], RandomTimeWait(), pyautogui.easeInOutQuad)
        pyautogui.click(btn_attaquer[0], btn_attaquer[1])
        pyautogui.moveTo(btn_trouver[0], btn_trouver[1], RandomTimeWait(), pyautogui.easeInOutQuad)
        pyautogui.click(btn_trouver[0], btn_trouver[1])

        # On attend de trouver un adversaire
        time.sleep(random.uniform(9, 12))

        # Vérifie s'il y a au moins un héros, demandé au user au début
        liste_trp = x_trp if heros else x_trp[:-1]
        x_trp_shuffle = RandomTrpClic(liste_trp)

        # On boucle sur le nombre de troupe pour les placer
        for j in range(len(x_trp_shuffle)):
            spawn = RandomTrpSpawn()
            pyautogui.moveTo(x_trp_shuffle[j], y_trp, RandomTimeClic(), pyautogui.easeInOutQuad)
            pyautogui.click(x_trp_shuffle[j], y_trp)
            pyautogui.moveTo(x_trp_spawn[spawn], y_trp_spawn[spawn] , RandomTimeClic(), pyautogui.easeInOutQuad)
            pyautogui.click(x_trp_spawn[spawn], y_trp_spawn[spawn])

        # Active les capacités des troupes
        for j in range(len(liste_trp)):
            pyautogui.moveTo(liste_trp[j], y_trp, RandomTimeClic(), pyautogui.easeInOutQuad)
            pyautogui.click(liste_trp[j], y_trp)

        # Patiente un peu
        time.sleep(random.uniform(2, 4))

        # Abandonne l'attaque et rentre
        pyautogui.moveTo(btn_capituler[0], btn_capituler[1], RandomTimeClic(), pyautogui.easeInOutQuad)
        pyautogui.click(btn_capituler[0], btn_capituler[1])
        pyautogui.moveTo(btn_capituler_ok[0], btn_capituler_ok[1], RandomTimeClic(), pyautogui.easeInOutQuad)
        pyautogui.click(btn_capituler_ok[0], btn_capituler_ok[1])
        pyautogui.moveTo(btn_rentrer[0], btn_rentrer[1], RandomTimeClic(), pyautogui.easeInOutQuad)
        pyautogui.click(btn_rentrer[0], btn_rentrer[1])

        # Patiente un peu
        time.sleep(random.uniform(4, 6))

        # Calcule le temps et l'affiche
        end_time = time.time()
        temps = round(end_time - start_time, 2)
        print("     Fin, temps écoulé : " + str(temps) + "s")
        compteur += 1
        time.sleep(1)
    print("--------------------------------")

    # Scroll pour aller vers la charette à Elixir
    pyautogui.moveTo(700,300,RandomTimeClic(), pyautogui.easeInOutQuad)
    time.sleep(0.2)
    pyautogui.mouseDown(button='left')
    time.sleep(0.2)
    pyautogui.moveTo(700,500,RandomTimeClic(), pyautogui.easeInOutQuad)
    pyautogui.mouseUp(button='left')

    
    try:
        # Cherche l'image de la charette à elixir
        charette_x, charette_y = pyautogui.locateCenterOnScreen(image_charette, confidence=0.6)
        pyautogui.moveTo(charette_x, charette_y, RandomTimeClic(), pyautogui.easeInOutQuad)
        pyautogui.click(charette_x, charette_y)

        time.sleep(1)
        
        # Recupere l'elixir 
        pyautogui.moveTo(btn_recuperer_charette[0], btn_recuperer_charette[1], RandomTimeClic(), pyautogui.easeInOutQuad)
        pyautogui.click(btn_recuperer_charette[0], btn_recuperer_charette[1])
        pyautogui.moveTo(btn_quitter_charette[0], btn_quitter_charette[1], RandomTimeClic(), pyautogui.easeInOutQuad)
        pyautogui.click(btn_quitter_charette[0], btn_quitter_charette[1])

        print("Elixir récupéré !")

    except pyautogui.ImageNotFoundException:
        print("Charette à élixir pas trouvé, on passe à la suite")
    


