import csv
from math import sqrt
from random import randint

EXAMPLES = [{'Courage': 9, 'Ambition': 2, 'Intelligence': 8, 'Good': 9},
            {'Courage': 6, 'Ambition': 7, 'Intelligence': 9, 'Good': 7},
            {'Courage': 3, 'Ambition': 8, 'Intelligence': 6, 'Good': 3},
            {'Courage': 2, 'Ambition': 3, 'Intelligence': 7, 'Good': 8},
            {'Courage': 3, 'Ambition': 4, 'Intelligence': 8, 'Good': 8}]
k = 5

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

    # return sqrt((perso2['Courage'] - perso1['Courage'])**2 + (perso2['Ambition'] - perso1['Ambition'])**2 + \
        # (perso2['Intelligence'] - perso1['Intelligence'])**2 + (perso2['Good'] - perso1['Good'])**2)
    return sqrt((perso2['Masse (kg)'] - perso1['Masse (kg)'])**2 + (perso2['Taille (cm)'] - perso1['Taille (cm)'])**2)


def add_distances(tab: list, unknown_caracter: dict) -> list:
    """
    Ajoute la distance par rapport à un personnage cible sur tous les personnage

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
        if neighbour['Poste'] in houses:
            houses[neighbour['Poste']] += 1
        else:
            houses[neighbour['Poste']] = 1
    max = 0
    for house, n in houses.items():
        if n > max:
            max = n
            best_house = house
    return best_house


def test_data(tab: list) -> list:
    """
    Renvoie les 3 quarts des éléments de la liste en enlevant aléatoirement le quart

    Entrée: Une liste de personnages
    Sortie: Une liste contenant les 3/4 de la liste originelle
    """

    joueurs_test = []
    copie_joueurs = tab[:]
    for _ in range(len(copie_joueurs) // 4):
        joueurs_test.append(copie_joueurs.pop(randint(0, len(copie_joueurs) - 1)))
    return joueurs_test, copie_joueurs


def best_k(tab: list) -> int:
    """
    Calcule le nombre de voisins donnant le résultat le plus précis pour une personne inconnue

    Entrée: Une liste de personnages
    Sortie: Le nombre de voisins le plus précis
    """

    nb_test = 100
    best = 0
    for k in range(1, 20):
        guessed_right = 0
        print(f"Calculating % of sucess with {k} neighbour{'s' if k > 1 else ''}...")
        for test in range(nb_test):
            caracters_test, reference_caracters = test_data(tab)
            for target in caracters_test:
                reference_caracters = add_distances(reference_caracters, target)
                neighbours = sorted(reference_caracters, key=lambda x: x['Distance'])
                if best_house(neighbours[:k]) == target['Poste']:
                    guessed_right += 1
        if guessed_right > best:
            best_k = k
            best = guessed_right
        print(f"With {k} neighbour{'s' if k > 1 else ''} we have {round(guessed_right/nb_test, 2)}% of sucess")
    return best_k


def house(tab: list, caracter: dict, k: int) -> str:
    """
    Calcule la meilleur maison pour un personnage inconnu en fonction
    du nombre de voisins sélectionnés

    Entrée: Une liste de personnages
            Le personnage pour lequel on détermine sa maison
            Le nombre de voisins pris en compte pour le calcul
    Sortie: La meilleur maison pour le personnage
            Ses k plus proches voisins
    """

    caracters = add_distances(tab, caracter)
    neighbours = sorted(caracters, key=lambda x: x['Distance'])
    return best_house(neighbours[:k]), neighbours[:k]


def main():
    # for ex in EXAMPLES:
    #     house, neighbours = house(caracters, ex, k)
    #     print(f"Vos voisins: {neighbours}\n Permettent de nous faire penser que vous ferez partie de {house}.")
    k = best_k(joueurs)
    print(f"Best k = {k}")

main()