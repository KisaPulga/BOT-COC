import time
import pyautogui
import os
import random
import pytesseract
from PIL import Image

# Lien vers pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("Mettez la souris en haut a gauche de la fenetre")
time.sleep(3)
x_gauche_user, y_gauche_user = pyautogui.position()
print("Mettez la souris en bas a droite de la fenetre")
time.sleep(3)
x_droite_user, y_droite_user = pyautogui.position()

x_longueur_user = x_droite_user - x_gauche_user
y_longueur_user = y_droite_user - y_gauche_user


# Fenetre initiale
x_gauche_init = 0
y_gauche_init = 38
x_droite_init = 865
y_droite_init = 522

x_longueur_init = x_droite_init - x_gauche_init
y_longueur_init = y_droite_init - y_gauche_init

x_ratio = x_longueur_user / x_longueur_init


def Calcul_X_Y(x_base, y_base):
    x_ratio = (x_base - x_gauche_init) / x_longueur_init
    y_ratio = (y_base - y_gauche_init) / y_longueur_init

    new_x = x_gauche_user + x_ratio * x_longueur_user
    new_y = y_gauche_user + y_ratio * y_longueur_user

    return new_x,new_y


#############
# VARIABLES #
#############

# Boutons
btn_attaquer = Calcul_X_Y(50, 475)
btn_trouver = Calcul_X_Y(642, 360)
btn_capituler = Calcul_X_Y(52, 401)
btn_capituler_ok = Calcul_X_Y(511, 338)
btn_rentrer = Calcul_X_Y(432, 447)
btn_recuperer_charette = Calcul_X_Y(638, 445)
btn_quitter_charette = Calcul_X_Y(725, 87)

# Troupes
x_trp_init = [147, 213, 268, 326, 382, 439, 495]
y_trp = Calcul_X_Y(0,482)[1]
x_trp_user = [Calcul_X_Y(x, y_trp)[0] for x in x_trp_init]

trp_spawn_init = [
    (728,123),(778,360),(817,203),(737,383),
    (834,238),(796,314),(666,406),(83,326),
    (140,140),(43,289),(30,226),(175,395),
    (253,57),(595,423)
]
heros = False # a modifier si on a un héro

x_trp_spawn_user = []
y_trp_spawn_user = []

for x,y in trp_spawn_init:
    trp_x_user, trp_y_user = Calcul_X_Y(x,y)
    x_trp_spawn_user.append(trp_x_user)
    y_trp_spawn_user.append(trp_y_user)

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
        liste_trp = x_trp_user if heros else x_trp_user[:-1]
        x_trp_shuffle = RandomTrpClic(liste_trp)

        # On boucle sur le nombre de troupe pour les placer
        for j in range(len(x_trp_shuffle)):
            spawn = RandomTrpSpawn()
            pyautogui.moveTo(x_trp_shuffle[j], y_trp, RandomTimeClic(), pyautogui.easeInOutQuad)
            pyautogui.click(x_trp_shuffle[j], y_trp)
            pyautogui.moveTo(x_trp_spawn_user[spawn], y_trp_spawn_user[spawn] , RandomTimeClic(), pyautogui.easeInOutQuad)
            pyautogui.click(x_trp_spawn_user[spawn], y_trp_spawn_user[spawn])

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
    x_scroll_depart, y_scroll_depart = Calcul_X_Y(700,300)
    pyautogui.moveTo(x_scroll_depart,y_scroll_depart,RandomTimeClic(), pyautogui.easeInOutQuad)
    time.sleep(0.2)
    pyautogui.mouseDown(button='left')
    time.sleep(0.2)
    x_scroll_fin, y_scroll_fin = Calcul_X_Y(700,500)
    pyautogui.moveTo(x_scroll_fin,y_scroll_fin,RandomTimeClic(), pyautogui.easeInOutQuad)
    pyautogui.mouseUp(button='left')

    
    try:
        # redimensionne l'image en fonction des x / y du user
        image = Image.open(image_charette)
        nouvelle_largeur = int(image.width * x_ratio)
        nouvelle_hauteur = int(image.height * x_ratio)
        image_resized = image.resize((nouvelle_largeur, nouvelle_hauteur))
    
        charette_x, charette_y = pyautogui.locateCenterOnScreen(image_resized, confidence=0.6)
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
    


