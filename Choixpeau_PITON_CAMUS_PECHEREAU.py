import csv
from math import sqrt
from random import randint

with open("Joueurs_rugby_6_nations.csv", mode='r', encoding='utf-8') as f:
    dict_file = csv.DictReader(f, delimiter=';')
    joueurs = []
    for id, elt in enumerate(dict_file):
        joueurs.append({'Id': id})
        for key, value in elt.items():
            joueurs[id].update({key : (int(float(value)) if key == 'Masse (kg)' or key == 'Taille (cm)' or key == 'Age' else value)})


def distance(perso1: dict, perso2: dict) -> float:
    """
    Calcule la distance euclidienne entre deux personnages

    Entrée: Les deux personnages
    Sortie: La distance euclidienne entre les deux personnages
    """

    return sqrt((perso2['Courage'] - perso1['Courage'])**2 + (perso2['Ambition'] - perso1['Ambition'])**2 + \
        (perso2['Intelligence'] - perso1['Intelligence'])**2 + (perso2['Good'] - perso1['Good'])**2)


def add_distances(tab: list, unknown_caracter: dict) -> list:
    """
    Ajoute la distance par rapport à un joueur cible sur tous les joueurs

    Entrée: Un tableau de dictionnaires de chaque personnages
            Le personnage de référence pour le calcul des distances
    Sortie: Le tableau de dictionnaires avec les distances ajoutées
    """

    for joueur in tab:
        joueur['Distance'] = distance(unknown_caracter, joueur)
    return tab


def best_house(neighbours: list) -> str:
    """
    Renvoie la maison apparaissant le plus dans la liste des plus proches voisins

    Entrée: Liste des plus proches voisins
    Sortie: La maison apparaissant le plus parmis la liste des voisins
    """

    houses = {}
    for neighbour in neighbours:
        if neighbour['House'] in houses:
            neighbours[neighbour['House']] += 1
        else:
            neighbours[neighbour['House']] = 1
    max = 0
    for house, n in houses.items():
        if n > max:
            max = n
            best_house = house
    return best_house

def test_data(tab: list) -> list:
    joueurs_test = []
    copie_joueurs = tab[:]
    for _ in range(len(copie_joueurs) // 4):
        joueurs_test.append(copie_joueurs.pop(randint(0, len(copie_joueurs) - 1)))
    return joueurs_test, copie_joueurs