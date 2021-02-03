# import
from upemtk import *


# fonction
def lit_maps(nbr_m, ligne=[], colonne=[]):
    """
    permet de lire un fichier texte contenant une maps
    :param colonne: string
    :param ligne: string
    :param nbr_m: int
    :return:liste de deux liste de contraite
    """
    lst_maps = []
    maps_c = []
    if nbr_m != 0:
        fichier_maps = open("maps.txt", "r")
        for ligne1 in fichier_maps:
            lst_maps.append(ligne1.split("\n")[0])
    for i9 in [nbr_m * 2 - 2 + nbr_m - 1, nbr_m * 2 - 1 + nbr_m - 1]:
        if nbr_m != 0:
            maps_c.append(lst_maps[i9].split("/"))
        else:
            if i9 == -3:
                maps_c.append(ligne.split("/"))
            else:
                maps_c.append(colonne.split("/"))
        for i10 in range(len(maps_c[-1])):
            if len(maps_c[-1][i10]) > 2:
                maps_c[-1][i10] = maps_c[-1][i10].split("-")
                for i17 in range(len(maps_c[-1][i10])):
                    maps_c[-1][i10][i17] = int(maps_c[-1][i10][i17])
            elif len(maps_c[-1][i10]) <= 2:
                maps_c[-1][i10] = [int(maps_c[-1][i10])]
            else:
                for i11 in range(len(maps_c[-1][i10])):
                    maps_c[-1][i10][i11] = int(maps_c[-1][i10][i11])
    return maps_c


def affiche_cadrillage(x, y, nbr_r, nbr_c, taille):
    """
    permet d'afficher un cadrillage de maniere reccurssive
    :param x:int debut du cadrillage en haut a gauche
    :param y:int debut du cadrillage en haut a gauche
    :param nbr_r:int nombre de case en abscisse
    :param nbr_c:int nombre de case en ordonné
    :param taille: int taille d'une case en pixel
    :return: rien
    """
    for i1 in range(nbr_r):
        rectangle(x + (i1 * taille), y - 100, x + ((i1 + 1) * taille), y + (taille * (nbr_c)), epaisseur=2, tag="cadri")
    for i2 in range(nbr_c):
        rectangle(x - 100, y + (i2 * taille), x + (nbr_r * taille), y + (taille * (i2 + 1)), epaisseur=2, tag="cadri")


def affiche_plateau(lst, taille, x, y, ale):
    """
    affiche les cases pleine ou vide
    :param lst: liste
    :param taille: int
    :return:
    """
    for i3 in range(len(lst[0])):
        for i4 in range(len(lst)):
            if lst[i4][i3] == 1:
                affiche_remplir(x + i3 * taille, y + i4 * taille, "black", 1, taille)
            if lst[i4][i3] == 2:
                affiche_note(x + i3 * taille, y + i4 * taille, "black", 1, taille)
            if ale:
                mise_a_jour()


def affiche_restriction(lst1, lst2, taille, x, y):
    """
    affiche les contraites du plateau
    :param lst1: liste des contraintes des colonnes
    :param lst2: liste des contraintres des lignes
    :return:rien pour l'instant
    """
    for i5 in range(len(lst1)):
        for i6 in range(len(lst1[i5])):
            texte(x + (i5 * taille) + (taille // 2), y - 100 + ((100 / (len(lst1[i5]) + 1)) * (i6 + 1)),
                  str(lst1[i5][i6]),
                  ancrage="center", tag="restri")
    for i7 in range(len(lst2)):
        for i8 in range(len(lst2[i7])):
            texte(x - 100 + ((100 / (len(lst2[i7]) + 1)) * (i8 + 1)), y + (i7 * taille) + (taille // 2),
                  str(lst2[i7][i8]),
                  ancrage="center", tag="restri")


def affiche_jeu_plateau(lst1, lst2, plateau, x, y):
    """
    affiche le plateau avec toutes ses données
    :param lst1: liste des restriction des colonnes
    :param lst2: liste des restriction des lignes
    :param plateau: liste qui represente le plateau
    :param x: int
    :param y: int
    :return: rien pour l'instant
    """

    affiche_cadrillage(x, y, len(plateau[0]), len(plateau), taille_case)
    if complette_l_c(plateau, lst1, lst2):
        affiche_plateau(plateau, taille_case, x, y, False)
        rectangle(x - 100, y - 100, x + (len(plateau[0]) * taille_case), y + (len(plateau) * taille_case)
                  , couleur="red", epaisseur=3, tag="plateau")
        return True
    affiche_plateau(plateau, taille_case, x, y, False)
    rectangle(x - 100, y - 100, x + (len(plateau[0]) * taille_case), y + (len(plateau) * taille_case)
              , couleur="red", epaisseur=3, tag="plateau")
    affiche_restriction(lst1, lst2, taille_case, x, y)
    return False


def click(plateau, colonne2, ligne2, x, y, taille, posi_choix, dever):
    """
    permet de cliquer sur le plateau et change les cases
    :param dever: liste des niveau deverouiller
    :param posi_choix: liste de la position x , y du menu choix
    :param plateau: liste
    :param colonne2: liste
    :param ligne2: liste
    :param x: int
    :param y: int
    :param taille: int
    :return:
    """
    vic = False
    choix = 1
    while True:
        efface("choix")
        if affiche_jeu_plateau(colonne2, ligne2, plateau, x, y) and not vic:
            affiche_choix(posi_choix[0], posi_choix[1], choix + 1)
            attente(1)
            victoire(400, 320)
            attend_ev()
            efface("vic")
            lst_niv_dever[dever-1] = 2
            lst_niv_dever[dever] = 1
            modif_verouille(doc)
            vic = True
            niv_s(position_retour[0], position_retour[1])
        affiche_choix(posi_choix[0], posi_choix[1], choix + 1)
        ev = attend_clic_gauche()
        x1, y1 = ev
        if x < x1 < x + taille * len(plateau[0]) and y < y1 < y + taille * len(plateau) and not vic:
            x1, y1 = ((x1 - x) // taille, (y1 - y) // taille)
            if (plateau[y1][x1] == 1 or plateau[y1][x1] == 2) and (choix == 1 or choix == 2):
                liste_joue.append([x1, y1, plateau[y1][x1]])
                plateau[y1][x1] = 0
            else:
                liste_joue.append([x1, y1, 0])
                plateau[y1][x1] = choix
            # efface("choix")
        elif posi_choix[0] + 25 < x1 < posi_choix[0] + 75 and posi_choix[1] + 25 < y1 < posi_choix[
            1] + 75 and choix != 1 and not vic:
            choix = 1
        elif posi_choix[0] + 25 < x1 < posi_choix[0] + 75 and \
                posi_choix[1] + 125 < y1 < posi_choix[1] + 175 and choix != 2 and not vic:
            choix = 2
        elif position_pause[0] + 50 > x1 > position_pause[0] - 50 and \
                position_pause[1] + 50 > y1 > position_pause[1] - 50:
            plateau, m = menu(400, 300, plateau, ligne2, colonne2)
            if m:
                return False
        elif position_retour[0] + 50 > x1 > position_retour[0] - 50 and \
                position_retour[1] + 50 > y1 > position_retour[1] - 50:
            if not vic:
                plateau = efface_dernier(plateau, vic)
            else:
                return True
        elif position_indice[0] + 50 > x1 > position_indice[0] - 50 and \
                position_indice[1] + 50 > y1 > position_indice[1] - 50:
            imposible(300, 350)
            attente(2)
            efface("impo")
        else:
            pass


def efface_dernier(plateau, inf):
    """
    permet de revenir en arriere
    :param inf: inutile
    :param plateau: liste de liste
    :return: rien
    """
    if inf:
        imposible(300, 350)
        attente(2)
        efface("impo")
        return plateau
    else:
        if not liste_joue:
            imposible(300, 350)
            attente(2)
            efface("impo")
        else:
            plateau[liste_joue[-1][1]][liste_joue[-1][0]] = liste_joue[-1][2]
            liste_joue.pop(-1)
        return plateau


def imposible(x, y):
    """
    affiche un paneau impossible de centre x, y
    :param x: int
    :param y: int
    :return: rien
    """
    rectangle(x + 200, y + 100, x - 200, y - 100, remplissage="tomato", tag="impo")
    texte(x, y, liste_mots_l[3], taille=50, ancrage="center", tag="impo")


def map_blanche(r_colonne, r_ligne):
    """
    permet de former une map vide de la taille des restrictions
    :param r_colonne: liste
    :param r_ligne: liste
    :return: list de liste
    """
    maps = []
    for i12 in range(len(r_ligne)):
        maps.append([0] * len(r_colonne))
    return maps


def affiche_remplir(x, y, couleur, px, taille):
    """
    permet d'afficher un rectangle noir dont le coin en haut a gauche a pour coordoner x, y
    :param px: int
    :param x: int
    :param y: int
    :param couleur: string, couleur des bordures
    :return: rien
    """
    rectangle(x, y, x + taille, y + taille, couleur=couleur, remplissage="black", epaisseur=px, tag="choix")


def affiche_note(x, y, couleur, px, taille):
    """
    permet d'afficher une croix noire dont le coin en haut a gauche a pour coordoner x, y
    :param px: int
    :param x: int
    :param y: int
    :param couleur: string, couleur des bordures
    :return: rien
    """
    rectangle(x, y, x + taille, y + taille, couleur=couleur, epaisseur=px, tag="choix")
    polygone([[x, y], [x + (taille / 2), y + (taille / 2)], [x + taille, y],
              [x + (taille / 2), y + (taille / 2)], [x + taille, y + taille],
              [x + (taille / 2), y + (taille / 2)], [x, y + taille],
              [x + (taille / 2), y + (taille / 2)]], epaisseur=1, couleur="red", tag="choix")


def affiche_choix(x, y, choix):
    """
    affiche ce que l'on va afficher sur la grille
    :param x: int
    :param y: int
    :param choix: int
    :return: rien
    """
    couleur_c = ["red", "black"]
    rectangle(x, y, x + 100, y + 200, couleur="black", remplissage="white", epaisseur=3)
    affiche_remplir(x + 25, y + 25, couleur_c[choix % 2], 3, 50)
    affiche_note(x + 25, y + 125, couleur_c[(choix + 1) % 2], 3, 50)


def donne_taille(ligne, colonne):
    """
    permet de donner la taille des cases de la taille optimal
    :param ligne: liste
    :param colonne: liste
    :return: min(450 // len(ligne), 400 // len(colonne))
    """
    return min(450 // len(ligne), 500 // len(colonne))


def complette_l_c(plat, col, lig):
    """
    permet de savoir si toutes les conditions son remplis
    :param plat: liste de liste
    :param col: liste de restriction pour les colonnes
    :param lig: liste de restriction pour les lignes
    :return: True si toutes les restrictions sont validées sinon return False
    """
    lst_condi1 = []
    for i13 in range(len(plat)):
        lst_condi1.append(test_li(plat, lig[i13], i13, test=[]))
        if lst_condi1[i13]:
            complette_li(plat, i13)
    lst_condi2 = []
    for i15 in range(len(plat[0])):
        lst_condi2.append(test_col(plat, col[i15], i15, test2=[]))
        if lst_condi2[i15]:
            complette_col(plat, i15)
    # print(lst_condi)
    if False not in lst_condi1 and False not in lst_condi2:
        return True
    else:
        return False


def test_li(plateau, restrie, ligne, compt=0, bool=0, nbr_b=0, test=[]):
    """
    permet de tester si la ligne designé remplis les conditions saisie
    :param plateau: liste de liste constituant le plateau
    :param restrie: liste de la restriction a tester
    :param ligne: numero de la ligne a tester
    :param compt: int rang dans la liste
    :param bool: suite de carré noir =1 suite de carré blanc=0
    :param nbr_b: int designe le numero de la suite de block
    :param test: liste qui enregistre les groupes noirs
    :return:True si la condition est remplit sinon False
    """
    if compt == len(plateau[0]):
        if restrie == 0:
            return test
        else:
            if not test:
                test = [0]
            if test == restrie:
                return True
            else:
                return False
    else:
        if plateau[ligne][compt] == 1:
            if compt == 0:
                test.append(1)
                return test_li(plateau, restrie, ligne, compt + 1, 1, nbr_b, test)
            else:
                if bool == 1:
                    test[nbr_b] += 1
                    return test_li(plateau, restrie, ligne, compt + 1, 1, nbr_b, test)
                else:
                    test.append(1)
                    return test_li(plateau, restrie, ligne, compt + 1, 1, nbr_b, test)
        else:
            if plateau[ligne][compt - 1] == 1 and compt != 0:
                return test_li(plateau, restrie, ligne, compt + 1, 0, nbr_b + 1, test)
            else:
                return test_li(plateau, restrie, ligne, compt + 1, 0, nbr_b, test)


def complette_li(plateau, ligne):
    """
    complete  les autres case par des croix  lorsqu'une ligne remplit ses conditions
    :param plateau: liste de liste
    :param ligne: int donne le numero de la liste
    :return:
    """
    for i14 in range(len(plateau[0])):
        if plateau[ligne][i14] != 1:
            plateau[ligne][i14] = 2


def test_col(plateau, restric, colonne, compt2=0, bool2=0, nbr_b_c=0, test2=[]):
    """
    permet de tester si la ligne designée remplit les conditions saisie
    :param test2: liste qui enregistre les groupes noirs
    :param colonne: designe la colonne qui va etre testé
    :param plateau: liste de liste constituant le plateau
    :param restric: liste de la restriction a tester
    :param compt2: int rang dans la liste
    :param bool2: suite de carré noir =1 suite de carré blanc=0
    :param nbr_b_c: int designe le numero de la suite de block
    :return:True si la condition est remplit sinon False
    """
    if compt2 == len(plateau):
        if restric == 0:
            return test2
        else:
            if not test2:
                test2 = [0]
            if test2 == restric:
                return True
            else:
                return False
    else:
        if plateau[compt2][colonne] == 1:
            if compt2 == 0:
                test2.append(1)
                return test_col(plateau, restric, colonne, compt2 + 1, 1, nbr_b_c, test2)
            else:
                if bool2 == 1:
                    test2[nbr_b_c] += 1
                    return test_col(plateau, restric, colonne, compt2 + 1, 1, nbr_b_c, test2)
                else:
                    test2.append(1)
                    return test_col(plateau, restric, colonne, compt2 + 1, 1, nbr_b_c, test2)
        else:
            if plateau[compt2 - 1][colonne] == 1 and compt2 != 0:
                return test_col(plateau, restric, colonne, compt2 + 1, 0, nbr_b_c + 1, test2)
            else:
                return test_col(plateau, restric, colonne, compt2 + 1, 0, nbr_b_c, test2)


def complette_col(plateau, colonne):
    """
    complete les autres case par des croix lorsqu'une ligne remplit ses conditions
    :param plateau: liste de liste
    :param colonne: int donne le numero de la liste
    :return:
    """
    for i16 in range(len(plateau)):
        if plateau[i16][colonne] != 1:
            plateau[i16][colonne] = 2


def bouton(x, y, txt):
    """
    affiche un bouton avec le texte de centre x,y
    :param x: int ordonnées
    :param y: int abcisse
    :param txt: str texte a afficher
    """
    rectangle(x - 100, y - 30, x + 100, y + 30, tag='bouton', couleur='black', remplissage="light grey", epaisseur=2)
    texte(x, y, txt, ancrage="center", taille=18, tag='bouton', police='comic sans ms')


def menu(x, y, plateau, lig_con, col_con):
    """
    affiche le menus et les boutons
    :param plateau: liste de liste qui donne la maps
    :param x: int ordonnées
    :param y: int abscisse
    :return: rien pour l'instant
    """
    reprendre = [x, y - 50]
    changer = [x, y + 50]
    recommencer = [x, y + 150]
    quitter = [x, y + 250]
    rectangle(x - 200, y - 250, x + 200, y + 350, tag='menus', epaisseur=5, couleur='black', remplissage="cornsilk")
    bouton(recommencer[0], recommencer[1], liste_mots_l[11])
    bouton(quitter[0], quitter[1], liste_mots_l[12])
    bouton(changer[0], changer[1], liste_mots_l[10])
    bouton(reprendre[0], reprendre[1], liste_mots_l[9])
    texte(x, y - 150, liste_mots_l[8], ancrage="center", police='comic sans ms', tag='menus')
    while True:
        ev = attend_clic_gauche()
        if reprendre[0] - 100 < ev[0] < reprendre[0] + 100 and reprendre[1] - 30 < ev[1] < reprendre[1] + 30:
            efface("bouton")
            efface("menus")
            return plateau, False
            # reprendre la partie
        elif changer[0] - 100 < ev[0] < changer[0] + 100 and changer[1] - 30 < ev[1] < changer[1] + 30:
            efface_tout()
            return plateau, True
            # proposer le changement de map
        elif recommencer[0] - 100 < ev[0] < recommencer[0] + 100 and recommencer[1] - 30 < ev[1] < recommencer[1] + 30:
            efface("bouton")
            efface("menus")
            return map_blanche(col_con, lig_con), False
            # recommencer la partie
        elif quitter[0] - 100 < ev[0] < quitter[0] + 100 and quitter[1] - 30 < ev[1] < quitter[1] + 30:
            exit()
        else:
            pass


def pause(x, y):
    """
    affiche le bouton pause de centre x, y
    :param x: int
    :param y: int
    :return: rien
    """
    rectangle(x + 50, y + 50, x - 50, y - 50, remplissage="white")
    rectangle(x + 20, y + 20, x + 8, y - 20, remplissage="grey")
    rectangle(x - 20, y + 20, x - 8, y - 20, remplissage="grey")


def menu_debu():
    """
    affiche le menu et permet de choisir ce qu l'on va faire
    :return:
    """
    posi_crea = [475, 400]
    posi_hist = [175, 400]
    while True:
        efface("acceuil")
        retour(position_retour[0], position_retour[1], "green")
        fonction_alleatoire(posi_hist[0], posi_hist[1], liste_mots_l[4])
        fonction_alleatoire(posi_crea[0], posi_crea[1], liste_mots_l[5])
        ev1 = attend_clic_gauche()
        if posi_hist[0] - 125 < ev1[0] < posi_hist[0] + 125 and posi_hist[1] - 200 < ev1[1] < posi_hist[1] + 200:
            efface("acceuil")
            niveau_c = affiche_niveaux(nombre_de_maps, lst_niv_dever)
            if not niveau_c:
                efface("niveau")
                efface("r")
                continue
            efface("niveau")
            return True, niveau_c
        elif posi_crea[0] - 125 < ev1[0] < posi_crea[0] + 125 and posi_crea[1] - 200 < ev1[1] < posi_crea[1] + 200:
            efface("acceuil")
            if not chooix_ds_crea():
                efface("r")
        elif position_retour[0] + 50 > ev1[0] > position_retour[0] - 50 and \
                position_retour[1] + 50 > ev1[1] > position_retour[1] - 50:
            return False, ""
        else:
            pass


def change_page(x, y, nbr):
    """
    affiche la langue choisie et les fleche pour la changer de centre x, y
    :param nbr: int
    :param x: int
    :param y: int
    :return: rien
    """
    rectangle(x + 85, y + 20, x - 85, y - 20, remplissage="white", tag="niveau")
    texte(x - 55, y - 15, "".join(["page nº", str(nbr)]), tag="niveau")
    rectangle(x + 95, y + 20, x + 140, y - 20, remplissage="white", tag="niveau")
    polygone([(x + 100, y + 15), (x + 100, y - 15),
              (x + 135, y)], epaisseur=3, tag="niveau")
    rectangle(x - 95, y + 20, x - 140, y - 20, remplissage="white", tag="niveau")
    polygone([(x - 100, y + 15), (x - 100, y - 15),
              (x - 135, y)], epaisseur=3, tag="niveau")


def affiche_niveaux(maxim, dispo):
    """
    affiche les diffent niveau disponible
    :param dispo: liste donne si un niveau est accecible
    :param maxim: int nombre de niveau posible
    :return: int le niveau choisie
    """
    nbr_page = 1
    posi_nive = [[175, 200], [475, 200], 300]
    posi_page = [350, 650]
    retour(position_retour[0], position_retour[1], "green")
    while True:
        change_page(posi_page[0], posi_page[1], nbr_page)
        for i1 in range(2):
            niveaux(posi_nive[0][0], posi_nive[0][1] + posi_nive[2] * i1,
                    " ".join([liste_mots_l[6], str(i1 + 1 + (4 * (nbr_page - 1)))]), dispo[4 * (nbr_page - 1)+i1])
            niveaux(posi_nive[1][0], posi_nive[1][1] + posi_nive[2] * i1,
                    " ".join([liste_mots_l[6], str(i1 + 3 + (4 * (nbr_page - 1)))]), dispo[2 + (4 * (nbr_page - 1))+i1])
        ev = attend_clic_gauche()
        if posi_page[0] + 95 < ev[0] < posi_page[0] + 140 and posi_page[1] - 20 < ev[1] < posi_page[
            1] + 20 and nbr_page < maxim / 4:
            nbr_page = nbr_page + 1
        elif posi_page[0] - 95 > ev[0] > posi_page[0] - 140 and posi_page[1] - 20 < ev[1] < posi_page[
            1] + 20 and nbr_page > 1:
            nbr_page = nbr_page - 1
        #
        elif posi_nive[0][0] - 100 < ev[0] < posi_nive[0][0] + 100 and \
                posi_nive[0][1] - 100 < ev[1] < posi_nive[0][1] + 100 and\
                (dispo[4 * (nbr_page - 1)] == 1 or dispo[4 * (nbr_page - 1)] == 2):
            return 1 + (4 * (nbr_page - 1))
        elif posi_nive[1][0] - 100 < ev[0] < posi_nive[1][0] + 100 and \
                posi_nive[1][1] - 100 < ev[1] < posi_nive[1][1] + 100 and\
                (dispo[2+(4 * (nbr_page - 1))] == 1 or dispo[2+(4 * (nbr_page - 1))] == 2):
            return 3 + (4 * (nbr_page - 1))
        elif posi_nive[0][0] - 100 < ev[0] < posi_nive[0][0] + 100 and \
                posi_nive[0][1] - 100 + posi_nive[2] < ev[1] < posi_nive[0][1] + 100 + posi_nive[2] and\
                (dispo[1 + (4 * (nbr_page - 1))] == 1 or dispo[1 + (4 * (nbr_page - 1))] == 2):
            return 2 + (4 * (nbr_page - 1))
        elif posi_nive[1][0] - 100 < ev[0] < posi_nive[1][0] + 100 and \
                posi_nive[1][1] - 100 + posi_nive[2] < ev[1] < posi_nive[1][1] + 100 + posi_nive[2] and\
                (dispo[3 + (4 * (nbr_page - 1))] == 1 or dispo[3 + (4 * (nbr_page - 1))] == 2):
            return 4 + (4 * (nbr_page - 1))
        #
        elif position_retour[0] + 50 > ev[0] > position_retour[0] - 50 and \
                position_retour[1] + 50 > ev[1] > position_retour[1] - 50:
            return False
        else:
            pass


def fonction_alleatoire(x, y, txt, nom_fichier=None):
    """
    affiche un rectangle avec le texte txt en bas et une image si nom_fichier est rempli
    :param x: int
    :param y: int
    :param txt: string
    :param nom_fichier: string
    :return: rien
    """
    rectangle(x - 125, y - 200, x + 125, y + 200, remplissage="white", epaisseur=3, tag="acceuil")
    rectangle(x - 125, y + 130, x + 125, y + 200, remplissage="black", tag="acceuil")
    if nom_fichier is not None:
        image(x, y - 30, nom_fichier, ancrage="center", tag="acceuil")
    texte(x, y + 160, txt, couleur="white", ancrage="center", tag="acceuil")


def niveaux(x, y, txt, bool):
    """
    affiche une case de centre x, y avec le niveau qu'elle represente
    :param x: int
    :param y: int
    :param txt: string
    :return: rien
    """
    if bool == 0:
        rectangle(x - 100, y - 100, x + 100, y + 100, remplissage="lightgrey", epaisseur=3, tag="niveau")
    else:
        rectangle(x - 100, y - 100, x + 100, y + 100, remplissage="white", epaisseur=3, tag="niveau")
    if bool == 2:
        rectangle(x+50, y-30, x-50, y+30, couleur="red",epaisseur=3, tag="niveau")
        texte(x, y, "FINI", ancrage="center", couleur="red", tag="niveau")
    rectangle(x - 100, y + 50, x + 100, y + 100, remplissage="Black", tag="niveau")
    texte(x, y + 75, txt, ancrage="center", couleur="white", tag="niveau")


def indice(x, y):
    """
    affiche une ampoule qui signifie si l'utilisateur veux un indice de centre x, y
    :param x: int
    :param y: int
    :return: rien
    """
    rectangle(x + 50, y + 50, x - 50, y - 50, remplissage="white", tag="indice")
    cercle(x, y - 10, 15, remplissage="yellow", tag="indice")
    polygone([(x - 7, y + 4), (x + 7, y + 4), (x + 5, y + 15), (x + 1, y + 20), (x - 1, y + 20), (x - 5, y + 15)],
             remplissage="grey", tag="indice")


def retour(x, y, couleur):
    """
    permet d'afficher un bouton reour de centre x, y
    :param x: int
    :param y: int
    :return: rien
    """
    rectangle(x + 50, y + 50, x - 50, y - 50, remplissage="white", tag="r")
    cercle(x, y, 25, remplissage=couleur, tag="r")
    cercle(x, y, 15, remplissage="white", tag="r")
    rectangle(x, y + 40, x - 40, y - 40, remplissage="white", couleur="white", tag="r")
    rectangle(x, y + 15, x - 15, y + 25, remplissage=couleur, tag="r")
    rectangle(x, y + 16, x - 14, y + 24, remplissage=couleur, couleur=couleur, tag="r")
    polygone([(x, y - 5), (x, y - 35), (x - 15, y - 20)], remplissage=couleur, tag="r")
    rectangle(x, y - 16, x, y - 24, couleur=couleur, tag="r")


def niv_s(x, y):
    """
    affiche un bouton pour demander si l'on veux aller au niveau suivant
    :param x: int
    :param y: int
    :return: rien
    """
    rectangle(x + 50, y + 50, x - 50, y - 50, remplissage="white", tag="r")
    if lan_d == 0:
        texte(x, y, "".join([liste_mots_l[6], "\n", liste_mots_l[13]]), ancrage="center", tag="r")
    else:
        texte(x, y, "".join([liste_mots_l[13], "\n", liste_mots_l[6]]), ancrage="center", tag="r")


def victoire(x, y):
    """
    affiche le logo lors de la victoire de centre x, y
    :param x: int
    :param y: int
    :return: rien
    """
    # fond:
    rectangle(x - 375, y - 225, x + 375, y + 300, remplissage="cornsilk", epaisseur=3, tag="vic")
    # rubi millieux
    polygone([(x - 50, y), (x, y - 75), (x + 50, y), (x, y + 75)], remplissage="yellow", tag="vic")
    # le "v"
    polygone([(x, y + 100), (x + 100, y - 50), (x + 250, y - 50), (x + 250, y - 50), (x + 225, y - 20),
              (x + 130, y - 20), (x + 25, y + 135), (x - 25, y + 135), (x - 130, y - 20), (x - 225, y - 20),
              (x - 250, y - 50), (x - 100, y - 50)], remplissage="mediumblue", tag="vic")
    # chapeau du rubi
    polygone([(x, y - 100), (x + 60, y - 10), (x + 87, y - 50), (x, y - 200), (x - 87, y - 50), (x - 60, y - 10)],
             remplissage="orange", tag="vic")
    # aille droite
    polygone([(x + 140, y - 10), (x + 40, y + 135), (x + 100, y + 135),
              (x + 350, y - 50), (x + 260, y - 50), (x + 225, y - 10)], remplissage="darkorange", tag="vic")
    # aile gauche
    polygone([(x - 140, y - 10), (x - 40, y + 135), (x - 100, y + 135),
              (x - 350, y - 50), (x - 260, y - 50), (x - 225, y - 10)], remplissage="darkorange", tag="vic")
    # texte
    texte(x, y + 200, liste_mots_l[20], ancrage="center", taille=100, tag="vic")


def chooix_ds_crea():
    """
    permet de choisir quel mode dans le mode createur nous allons choisir
    :return: rien pour l'instant
    """
    posi_restri = [475, 400]
    posi_carreau = [175, 400]
    while True:
        fonction_alleatoire(posi_restri[0], posi_restri[1], liste_mots_l[14])
        fonction_alleatoire(posi_carreau[0], posi_carreau[1], liste_mots_l[15])
        retour(position_retour[0], position_retour[1], "green")
        ev = attend_clic_gauche()
        if posi_restri[0] - 125 < ev[0] < posi_restri[0] + 125 and posi_restri[1] - 200 < ev[1] < posi_restri[1] + 200:
            efface("acceuil")
            validation , contrainte = rentre_restrie()
            if validation:
                print(lit_maps(0, contrainte[0], contrainte[1]))
                #solveur
            efface("clavier")
        elif posi_carreau[0] - 125 < ev[0] < posi_carreau[0] + 125 and posi_carreau[1] - 200 < ev[1] < posi_carreau[
            1] + 200:
            efface("acceuil")
            #####
            # rajoute ton truc ici ou envois moi en teste et je le ferait
            #
            ####
            print("creation maps")
        elif position_retour[0] + 50 > ev[0] > position_retour[0] - 50 and \
                position_retour[1] + 50 > ev[1] > position_retour[1] - 50:
            return False
        else:
            pass


def rentre_restrie():
    """
    affiche la page pour rentrer ses contrainte
    :return: uniquement False
    """
    taille = 650//14
    barre_ligne = [10, 230, 600, 270]
    barre_colonne = [10, 330, 600, 370]
    valider = [300, 600]
    lst_ligne = [""]
    lst_colonne = [""]
    bouton(300, 125, liste_mots_l[16])
    bouton(300, 600, liste_mots_l[19])
    texte(10, 200, liste_mots_l[17], ancrage="w", tag="c_res")
    texte(10, 300, liste_mots_l[18], ancrage="w", tag="c_res")
    rectangle(10, 230, 600, 270, remplissage="white", epaisseur=3, tag="c_res")
    rectangle(10, 330, 600, 370, remplissage="white", epaisseur=3, tag="c_res")
    clavier(taille)
    while True:
        efface("entre")
        texte(20, 250, "".join(lst_ligne), ancrage="w", tag="li")
        texte(20, 350, "".join(lst_colonne), ancrage="w", tag="co")
        ev = attend_clic_gauche()
        if barre_ligne[0] < ev[0] < barre_ligne[2] and barre_ligne[1] < ev[1] < barre_ligne[3]:
            rectangle(10, 230, 600, 270, couleur="red", epaisseur=3, tag="indic")
            lst_ligne = note(lst_ligne, barre_ligne, taille)
            efface("indic")
            efface("li")
        elif barre_colonne[0] < ev[0] < barre_colonne[2] and barre_colonne[1] < ev[1] < barre_colonne[3]:
            rectangle(10, 330, 600, 370, couleur="red", epaisseur=3, tag="indic")
            lst_colonne = note(lst_colonne, barre_colonne, taille)
            efface("indic")
            efface("co")
        elif valider[0]-100 < ev[0] < valider[0] + 100 and valider[1]-30 < ev[1] < valider[1]+30:
            efface("c_res")
            efface("bouton")
            efface("co")
            efface("li")
            return True, ["".join(lst_ligne), "".join(lst_colonne)]
        elif position_retour[0] + 50 > ev[0] > position_retour[0] - 50 and \
                position_retour[1] + 50 > ev[1] > position_retour[1] - 50:
            efface("c_res")
            efface("bouton")
            efface("co")
            efface("li")
            return False, ""
        else:
            pass
    pass


def note(lst, coor, taille):
    """
    permet d'ecrire dans les case
    :param taille: int
    :param lst: liste qui donne le texte
    :param coor: liste donne les coordone de la ligne d'entrer
    :return: lst
    """
    clav = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "/"]
    while True:
        efface("entre")
        texte(20, coor[1] + 20, "".join(lst), ancrage="w", tag="entre")
        ev = attend_clic_gauche()
        for i1 in range(12):
            if taille*(i1+1)-20 < ev[0] < taille*(i1+1)+20 and 425-20 < ev[1] < 425+20:
                lst.append(clav[i1])
        if taille * (13.5) - 40 < ev[0] < taille * (13.5) + 20 and 425 - 20 < ev[1] < 425 + 20:
            if len(lst) > 1:
                lst.pop(-1)
            else:
                imposible(300, 350)
                attente(1)
                efface("impo")

        if coor[0] < ev[0] < coor[2] and coor[1] < ev[1] < coor[3] or 425-20 < ev[1] < 425+20:
            pass
        else:
            return lst
        mise_a_jour()


def clavier(taille):
    """
    affiche le clavier
    :param taille: int espace entre les bouton
    :return: rien
    """
    clav = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "/", ]
    for i2 in range(12):
        nbr(taille*(i2+1), 425, clav[i2])
    supre((taille*13)+(taille//2), 425)


def nbr(x, y, n):
    """
    affiche un petit bouton de centre x, y
    :param x: int
    :param y: int
    :param n: string ce qui est dans le bouton
    :return: rien
    """
    rectangle(x-20, y-20, x+20, y+20, remplissage="lightgrey", tag="clavier")
    texte(x, y, n, ancrage="center", tag="clavier")


def supre(x, y):
    """
    affichhe un boutron pour suprimer
    :param x: int
    :param y: int
    :return: rien
    """
    rectangle(x-20, y-20, x+20, y+20, remplissage="lightgrey", tag="clavier")
    polygone([(x-20, y-20), (x-20, y+20), x-40, y], remplissage="lightgrey", tag="clavier")
    rectangle(x - 20, y - 19, x + 19, y + 19, remplissage="lightgrey", couleur="lightgrey", tag="clavier")
    polygone([(x - 10, y - 10), (x + 10, y + 10), (x, y), (x + 10, y - 10), (x - 10, y + 10), (x, y)],
             remplissage="lightgrey", tag="clavier")


def intro(bool, langue_d):
    """
    affiche l'intro
    :return numero du dossier ouvere, liste des niveau debloquer
    """
    logi = [[1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1]]
    rectangle(0, 0, 800, 700, remplissage="cornsilk")
    y2 = 500
    if bool:
        y1 = 300
        rectangle(50, y1 - 50, 750, y1 + 150, remplissage="white", epaisseur=4, tag="int")
        affiche_plateau(logi, 15, 100, y1, True)
        while y1 > 100:
            efface("int")
            efface("choix")
            rectangle(50, y1-50, 750, y1 + 150, remplissage="white", epaisseur=4, tag="int")
            affiche_plateau(logi, 15, 100, y1, False)
            mise_a_jour()
            y1 -= 2
    else:
        rectangle(50, 50, 750, 250, remplissage="white", epaisseur=4, tag="int")
        affiche_plateau(logi, 15, 100, 100, False)
    liste_mot, langue_d = affiche_choix_langue(True, langue_d)
    print(liste_mot)
    efface("flag")
    niveaux(150, y2, liste_mot[0], 1)
    attente(0.1)
    niveaux(400, y2, liste_mot[1], 1)
    attente(0.1)
    niveaux(650, y2, liste_mot[2], 1)
    attente(0.1)
    while True:
        ev = attend_clic_gauche()
        for i in range(3):
            if 50 + (250 * i) < ev[0] < 250 + (250 * i) and y2 - 100 < ev[1] < y2 + 100:
                info = ouvre_doc(i + 1)
                return info[0], info[1], liste_mot, langue_d


def ouvre_doc(nbre):
    """
    ouvre de dossi numero nbre
    :param nbre: int
    :return: liste contenant les innfo du dossier
    """
    lst_info = []
    empla = open("".join(["place", str(nbre), ".txt"]), "r")
    for lign in empla:
        lst_info.append(list(lign.split("\n")[0]))
    for i in range(len(lst_info)):
        if len(lst_info[i]) == 1:
            lst_info[i] = int(lst_info[i][0])
        else:
            for i2 in range(len(lst_info[i])):
                lst_info[i][i2] = int(lst_info[i][i2])
    return lst_info


def modif_verouille(nbr_doss):
    """
    modifie le dissier sur le quel nous somme entrain de jouer
    :param nbr_doss: int
    :return: rien
    """
    lst_chang = []
    empla = open("".join(["place", str(nbr_doss), ".txt"]), "w")
    empla.write(str(nbr_doss))
    empla.write("\n")
    for i in lst_niv_dever:
        lst_chang.append(str(i))
    empla.write("".join(lst_chang))


def france(x, y, nbr):
    rectangle(x - (3/4)*nbr, y - (2/4)*nbr, x + (3/4)*nbr, y + (2/4)*nbr, remplissage="white", tag="flag")
    rectangle(x - (3/4)*nbr, y - (2/4)*nbr, x - (1/4)*nbr, y + (2/4)*nbr, remplissage="blue", tag="flag")
    rectangle(x + (3/4)*nbr, y - (2/4)*nbr, x + (1/4)*nbr, y + (2/4)*nbr, remplissage="red", tag="flag")


def anglai(x, y, nbr):
    rectangle(x - (3 / 4) * nbr, y - (2 / 4) * nbr, x + (3 / 4) * nbr, y + (2 / 4) * nbr, remplissage="mediumblue",
              tag="flag")

    polygone([(x - (3 / 4) * nbr, y - (2 / 4) * nbr), (x - (5 / 8) * nbr, y - (2 / 4) * nbr),
              (x, y - (1 / 8) * nbr), (x + (5 / 8) * nbr, y - (2 / 4) * nbr), (x + (3 / 4) * nbr, y - (2 / 4) * nbr),
              (x + (3 / 4) * nbr, y - (3 / 8) * nbr), (x + (1 / 8) * nbr, y), (x + (3 / 4) * nbr, y + (3 / 8) * nbr),
              (x + (3 / 4) * nbr, y + (2 / 4) * nbr), (x + (5 / 8) * nbr, y + (2 / 4) * nbr), (x, y + (1 / 8) * nbr),
              (x - (5 / 8) * nbr, y + (2 / 4) * nbr), (x - (3 / 4) * nbr, y + (2 / 4) * nbr),
              (x - (3 / 4) * nbr, y + (3 / 8) * nbr), (x - (1 / 8) * nbr, y), (x - (3 / 4) * nbr, y - (3 / 8) * nbr)],
             remplissage="white", tag="flag")

    polygone([(x - (3 / 4) * nbr, y - (2 / 4) * nbr), (x - (12 / 16) * nbr, y - (2 / 4) * nbr),
              (x, y - (1 / 16) * nbr), (x + (12 / 16) * nbr, y - (2 / 4) * nbr), (x + (3 / 4) * nbr, y - (2 / 4) * nbr),
              (x + (3 / 4) * nbr, y - (6.7 / 16) * nbr), (x + (1 / 16) * nbr, y), (x + (3 / 4) * nbr, y + (6.7 / 16) * nbr),
              (x + (3 / 4) * nbr, y + (2 / 4) * nbr), (x + (12 / 16) * nbr, y + (2 / 4) * nbr), (x, y + (1 / 16) * nbr),
              (x - (12 / 16) * nbr, y + (2 / 4) * nbr), (x - (3 / 4) * nbr, y + (2 / 4) * nbr),
              (x - (3 / 4) * nbr, y + (6.7 / 16) * nbr), (x - (1 / 16) * nbr, y),
              (x - (3 / 4) * nbr, y - (6.7 / 16) * nbr)], remplissage="red", tag="flag")

    polygone([(x - (3 / 16) * nbr, y - (2 / 4) * nbr), (x + (3 / 16) * nbr, y - (2 / 4) * nbr),
              (x + (3 / 16) * nbr, y - (3 / 16) * nbr),
              (x + (3 / 4) * nbr, y - (3 / 16) * nbr),
              (x + (3 / 4) * nbr, y + (3 / 16) * nbr),
              (x + (3 / 16) * nbr, y + (3 / 16) * nbr),
              (x + (3 / 16) * nbr, y + (2 / 4) * nbr),
              (x - (3 / 16) * nbr, y + (2 / 4) * nbr), (x - (3 / 16) * nbr, y + (3 / 16) * nbr),
              (x - (3 / 4) * nbr, y + (3 / 16) * nbr), (x - (3 / 4) * nbr, y - (3 / 16) * nbr),
              (x - (3 / 16) * nbr, y - (3 / 16) * nbr)], remplissage="white", couleur="white", tag="flag")

    polygone([(x - (2 / 16) * nbr, y - (2 / 4) * nbr), (x + (2 / 16) * nbr, y - (2 / 4) * nbr),
              (x + (2 / 16) * nbr, y - (2 / 16) * nbr),
              (x + (3 / 4) * nbr, y - (2 / 16) * nbr),
              (x + (3 / 4) * nbr, y + (2 / 16) * nbr),
              (x + (2 / 16) * nbr, y + (2 / 16) * nbr),
              (x + (2 / 16) * nbr, y + (2 / 4) * nbr),
              (x - (2 / 16) * nbr, y + (2 / 4) * nbr), (x - (2 / 16) * nbr, y + (2 / 16) * nbr),
              (x - (3 / 4) * nbr, y + (2 / 16) * nbr), (x - (3 / 4) * nbr, y - (2 / 16) * nbr),
              (x - (2 / 16) * nbr, y - (2 / 16) * nbr)], remplissage="red", couleur="black", tag="flag")

    rectangle(x - (3 / 4) * nbr, y - (2 / 4) * nbr, x + (3 / 4) * nbr, y + (2 / 4) * nbr,
              tag="flag")


def choix_langue(lagn):
    """
    ouvre le ficher qui donne la langue du jeu en fonction de lagn
    :param lagn: int
    :return: liste du texte dans la langue choisie
    """
    lst_des_langue = ["francais.txt", "anglais.txt"]
    fiche_lang = open(lst_des_langue[lagn], "r")
    lst_langue = []
    for ligne1 in fiche_lang:
        lst_langue.append(ligne1.split("\n")[0])
    return lst_langue


def affiche_choix_langue(intro, langue):
    x = 400
    y = 650
    posi_page = [400, 650]
    rectangle(x + 85, y + 20, x - 85, y - 20, remplissage="white", tag="flag")
    texte(x, y, "ok", ancrage="center", tag="flag")
    rectangle(x + 95, y + 20, x + 140, y - 20, remplissage="white", tag="flag")
    polygone([(x + 100, y + 15), (x + 100, y - 15),
              (x + 135, y)], epaisseur=3, tag="flag")
    rectangle(x - 95, y + 20, x - 140, y - 20, remplissage="white", tag="flag")
    polygone([(x - 100, y + 15), (x - 100, y - 15),
              (x - 135, y)], epaisseur=3, tag="flag")
    while True:
        if intro:
            if langue == 0:
                france(400, 450, 200)
            else:
                anglai(400, 450, 200)
        else:
            if langue == 0:
                france(700, 50, 75)
            else:
                anglai(700, 50, 75)
        ev = attend_clic_gauche()
        if posi_page[0] + 95 < ev[0] < posi_page[0] + 140 and posi_page[1] - 20 < ev[1] < posi_page[1] + 20:
            langue = (langue + 1) % 2
        elif posi_page[0] - 95 > ev[0] > posi_page[0] - 140 and posi_page[1] - 20 < ev[1] < posi_page[1] + 20:
            langue = (langue - 1) % 2
        elif posi_page[0] - 85 < ev[0] < posi_page[0] + 85 and posi_page[1] - 20 < ev[1] < posi_page[1] + 20:
            return choix_langue(langue), langue


#def solveur(plateau, con_li, con_col):

# variable globale
nombre_de_maps = 16
position_du_choix = [675, 110]
position_pause = [725, 375]
position_indice = [725, 500]
position_retour = [725, 625]
suivant = False
start = True
choix_langue(0)
lan_d = 0
liste_mots_l = []
# debut du code
cree_fenetre(800, 700)
while True:
    doc, lst_niv_dever, liste_mots_l, lan_d= intro(start, lan_d)
    print(liste_mots_l)
    start = False
    efface("int")
    efface("niv")
    while True:
        liste_joue = []
        rectangle(0, 0, 800, 700, remplissage="cornsilk")
        rectangle(650, 0, 800, 700, remplissage="light grey")
        rectangle(0, 0, 800, 75, remplissage="light grey")
        texte(100, 40, "LOGIMAGE", ancrage="center", taille=30)
        if suivant:
            nbr_map_c += 1
        else:
            conti, nbr_map_c = menu_debu()
            if not conti:
                break
        affiche_choix(position_du_choix[0], position_du_choix[1], 2)
        pause(position_pause[0], position_pause[1])
        indice(position_indice[0], position_indice[1])
        retour(position_retour[0], position_retour[1], "grey")
        restri = lit_maps(nbr_map_c)
        ligne, colonne = restri[0], restri[1]
        taille_case = donne_taille(ligne, colonne)
        suivant = click(map_blanche(colonne, ligne), colonne, ligne, 125, 200, taille_case, position_du_choix, nbr_map_c)
        # print(liste_joue)
