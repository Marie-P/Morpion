import time
from math import inf as infinity
from random import choice

#=============================================================================================#
#====================================== INITIALISATION =======================================#
#=============================================================================================#

Humain = -1
IA = +1

#=============================================================================================#
#========================================= FONCTIONS =========================================#
#=============================================================================================#

# Initialise de le morpion vide
def initMorpion(taille,grille):
    for i in range(0,taille):
        grille.append([])
        for j in range(0,taille):
            grille[i].append(0)
    return grille

# Fonction d'affichage
def affichageMorpion(grille,Ia_choix, Humain_choix):
    for line in grille:
        print('\t\t_ _ _ _ _ _ _ _ _ _ _ _ _ _\n\n\n\t\t |', end ='')
        for col in line:
            if col == +1:
                print("  ",Ia_choix, '  |',end='')
            elif col == -1:
                print("  ",Humain_choix, '  |',end='')
            else :
                print("  "," ", '  |',end='')
        print("\n")
    print('\t\t_ _ _ _ _ _ _ _ _ _ _ _ _ _')

# Vérifie les cases vides restantes
def casesVide(grille):
    cases = []

    for x, line in enumerate(grille):
        for y, col in enumerate(line):
            if col == 0: cases.append([x, y])
    return cases

# Vérifie quand les états sont empilés
def gagne(grille, joueur):

    possibilites = [
        [grille[0][0], grille[1][1], grille[2][2]],

        [grille[1][0], grille[1][1], grille[1][2]],

        [grille[2][0], grille[2][1], grille[2][2]],

        [grille[0][0], grille[1][0], grille[2][0]],

        [grille[0][0], grille[0][1], grille[0][2]],

        [grille[0][1], grille[1][1], grille[2][1]],

        [grille[0][2], grille[1][2], grille[2][2]],

        [grille[2][0], grille[1][1], grille[0][2]],
    ]
    if [joueur, joueur, joueur] in possibilites:
        return True
    else:
        return False

# Vérifie qui gagne
def finDePartie(grille):

    return gagne(grille, Humain) or gagne(grille, IA)

# Heuristique de victoire
def evaluation(grille):

    if gagne(grille, IA):
        score = +1
    elif gagne(grille, Humain):
        score = -1
    else:
        score = 0

    return score

# Vérifie les positions restantes
def positionsRestantes(x, y):

    if [x, y] in casesVide(morpion):
        return True
    else:
        return False

# Ajoute le coup du joueur dans le morpion
def ajoutDuChoix(x, y, joueur):

    if positionsRestantes(x, y):
        morpion[x][y] = joueur
        return True
    else:
        return False

# * * *  FONCTION MIN _MAX  * * *
def minimax(grille, profondeur, joueur):

    if joueur == IA:
        choix = [-1, -1, -infinity]
    else:
        choix = [-1, -1, +infinity]

    if profondeur == 0 or finDePartie(grille):
        score = evaluation(grille)
        return [-1, -1, score]

    for cell in casesVide(grille):
        x, y = cell[0], cell[1]
        grille[x][y] = joueur
        score = minimax(grille, profondeur - 1, -joueur)
        grille[x][y] = 0
        score[0], score[1] = x, y

        if joueur == IA:
            if score[2] > choix[2]:
                choix = score  
        else:
            if score[2] < choix[2]:
                choix = score  
                
    return choix

# Tours 
def ia_tour(Ia_choix, Humain_choix):

    nbCasesDisponibles = len(casesVide(morpion))
    if nbCasesDisponibles == 0 or finDePartie(morpion):
        return

    print('Ordinateur [O] '.format(Ia_choix))
    affichageMorpion(morpion, Ia_choix, Humain_choix)

    if nbCasesDisponibles == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        deplacement = minimax(morpion, nbCasesDisponibles, IA)
        x, y = deplacement[0], deplacement[1]

    ajoutDuChoix(x, y, IA)
    time.sleep(1)

def Humain_tour(Ia_choix, Humain_choix):
 
    nbCasesDisponibles = len(casesVide(morpion))
    if nbCasesDisponibles == 0 or finDePartie(morpion):
        return

    choix = -1
    choixPossibles = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    print("A l\'humain [{}]".format(Humain_choix))
    affichageMorpion(morpion, Ia_choix, Humain_choix)

    while (choix < 1 or choix > 9):
            choix = int(input('Choisir entre 1 et 9: '))
            coord = choixPossibles[choix]
            testDeplacement = ajoutDuChoix(coord[0], coord[1], Humain)
            if testDeplacement == False:
                print('Reessaye')
                choix = -1

#=============================================================================================#
#==================================== PROGRAMME PRINCIPAL ====================================#
#=============================================================================================#

morpion = initMorpion(3,[])

def main():
 
    Humain_choix = 'X'
    Ia_choix = 'O' 
    entree = ''  

    while entree != 'O' and entree != 'N':
        entree = input('Voulez vous commencer? O/N : ').upper()
        
    while len(casesVide(morpion)) > 0 and not finDePartie(morpion):
        # Dans le cas où l'IA commence
        if entree == 'N':
            ia_tour(Ia_choix, Humain_choix)
            entree = ''

        Humain_tour(Ia_choix, Humain_choix)
        ia_tour(Ia_choix, Humain_choix)

    # Si l'humaine gagne
    if gagne(morpion,Humain):
        print('Humain '.format(Humain_choix))
        affichageMorpion(morpion, Ia_choix, Humain_choix)
        print('Gagné')
    # Si l'IA gagne
    elif gagne(morpion, IA):
        print('Ordinateur '.format(Ia_choix))
        affichageMorpion(morpion, Ia_choix, Humain_choix)
        print('Perdu')
    # Si aucun des deux gagne
    else:
        affichageMorpion(morpion, Ia_choix, Humain_choix)
        print('Match Nul!')

    exit()

if __name__ == '__main__':
    main()