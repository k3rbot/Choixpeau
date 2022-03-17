# encoding: utf-8
# Projet Choixpeau Harry Potter 
# Réalisé par: Martin, Lou-Saya et Emil

import csv
from math import sqrt
from random import randint

from sklearn.metrics import jaccard_score

EXAMPLES = [{'Courage': 9, 'Ambition': 2, 'Intelligence': 8, 'Good': 9},
            {'Courage': 6, 'Ambition': 7, 'Intelligence': 9, 'Good': 7},
            {'Courage': 3, 'Ambition': 8, 'Intelligence': 6, 'Good': 3},
            {'Courage': 2, 'Ambition': 3, 'Intelligence': 7, 'Good': 8},
            {'Courage': 3, 'Ambition': 4, 'Intelligence': 8, 'Good': 8}]
k = 5

# Création de notre table contenant les personnages et leurs caractéristiques
# à partir de deux fichiers
with open("Characters.csv", mode='r', encoding='utf-8') as f:
        characters_file = csv.DictReader(f, delimiter=';')
        characters_prev = [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in characters_file]

with open("Caracteristiques_des_persos.csv", mode='r', encoding='utf-8') as g:
        characteristics_file = csv.DictReader(g, delimiter=';')
        characteristics = [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in characteristics_file]

characters = []
for char in characters_prev:
    for charact in characteristics:
        if char['Name'] == charact['Name']:
            characters.append(char)
            char['Courage'] = int(float(charact['Courage']))
            char['Intelligence'] = int(float(charact['Intelligence']))
            char['Good'] = int(float(charact['Good']))
            char['Ambition'] = int(float(charact['Ambition']))
            break


def distance(perso1: dict, perso2: dict) -> float:
    """
    Calcule la distance euclidienne entre deux personnages

    Entrée: Les deux personnages
    Sortie: La distance euclidienne entre les deux personnages
    """

    return sqrt((perso2['Courage'] - perso1['Courage'])**2 + (perso2['Ambition'] - perso1['Ambition'])**2 + \
        (perso2['Intelligence'] - perso1['Intelligence'])**2 + (perso2['Good'] - perso1['Good'])**2)


def add_distances(tab: list, unknown_character: dict) -> list:
    """
    Ajoute la distance par rapport à un personnage cible sur tous les personnage

    Entrée: Un tableau de dictionnaires de chaque personnages
            Le personnage de référence pour le calcul des distances
    Sortie: Le tableau de dictionnaires avec les distances ajoutées
    """

    for character in tab:
        character['Distance'] = distance(unknown_character, character)
    return tab


def best_house(neighbours: list) -> str:
    """
    Renvoie la maison apparaissant le plus dans la liste des plus proches voisins

    Entrée: Liste des plus proches voisins
    Sortie: La maison apparaissant le plus parmi la liste des voisins
    """

    houses = {}
    for neighbour in neighbours:
        if neighbour['House'] in houses:
            houses[neighbour['House']] += 1
        else:
            houses[neighbour['House']] = 1
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

    characters_test = []
    characters_copy = tab[:]
    for _ in range(len(characters_copy) // 4):
        characters_test.append(characters_copy.pop(randint(0, len(characters_copy) - 1)))
    return characters_test, characters_copy


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
        for _ in range(nb_test):
            characters_test, reference_characters = test_data(tab)
            for target in characters_test:
                char_house, neighbours = house_of(reference_characters, target, k)
                if char_house == target['House']:
                    guessed_right += 1
        if guessed_right > best:
            best_k = k
            best = guessed_right
        print(f"Avec {k} voisin{'s' if k > 1 else ''} nous avons {round(guessed_right/len(characters_test), 2)}% de succès.")
    return best_k


def house_of(tab: list, character: dict, k: int=5) -> str:
    """
    Calcule la meilleur maison pour un personnage inconnu en fonction
    du nombre de voisins sélectionnés

    Entrée: Une liste de personnages
            Le personnage pour lequel on détermine sa maison
            Le nombre de voisins pris en compte pour le calcul
    Sortie: La meilleur maison pour le personnage
            Ses k plus proches voisins
    """

    characters = add_distances(tab, character)
    neighbours = sorted(characters, key=lambda x: x['Distance'])
    return best_house(neighbours[:k]), neighbours[:k]


def new_profile() -> dict:
    """
    Demande à l'utilisateur des informations sur son personnage
    pour créer un profil

    Sortie : Le profil créé
    """

    profile = {}
    skills = {"Courage", "Ambition", "Intelligence", "Good"}
    for skill in skills :
        ok = False
        while not ok:
            try:
                value = int(input(f"Votre {skill if skill != 'Good' else 'Bonté'} entre 0 et 10 : "))
                if value > 10 or value < 0:
                    raise
                ok = True
            except:
                print("Entrez une valeur correcte")
        profile[skill] = value
    return profile


def main():
    """
    Boucle principale
    """
    choice = ''
    k = 5
    running = True
    
    while choice != 'n' and choice != 'y':
        choice = input("Voulez-vous utiliser le meilleur nombre de voisins ? (y/n) ")
    if choice == 'y':
        k = best_k(characters)
        print(f"Le meilleur nombre de voisins est {k}")
    else:
        choice = input("Voulez-vous modifier le nombre de voisins à prendre en compte ? (par défaut 5) (y/n) ")
        while choice != 'n' and choice != 'y':
            choice = input("Voulez-vous modifier le nombre de voisins à prendre en compte ? (par défaut 5) (y/n) ")
        if choice == 'y':
            ok = False
            while not ok:
                try:
                    k = int(input(f"Le nombre de voisins à prendre en compte: "))
                    ok = True
                except:
                    print("Entrez une valeur correcte")

    while running:
        choice = input("Voulez-vous créer un nouveau profil plutôt que d'afficher les exemples ? (y/n) ")
        while choice != 'n' and choice != 'y':
            choice = input("Voulez-vous créer un nouveau profil plutôt que d'afficher les exemples ? (y/n) ")
        if choice == 'y':
            profile = new_profile()
            house, neighbours = house_of(characters, profile, k)
            print("\nVos voisins:")
            for neighbour in neighbours:
                    print(f"{neighbour['Name']}: ", f"Bonté: {neighbour['Good']},", f"Intelligence: {neighbour['Intelligence']},",\
                            f"Ambition: {neighbour['Ambition']},", f"Courage: {neighbour['Courage'],}", f"Maison: {neighbour['House']}")
            print(f"\nNous apprennent dans quelle maison vous aurez le plus de chance d'aller : {house}.\n")
        elif choice == 'n':
            for ppl in EXAMPLES:
                house, neighbours = house_of(characters, ppl, k)
                print("\nAvec ces voisins :")
                for neighbour in neighbours:
                    print(neighbour['Name'], f"Bonté: {neighbour['Good']}", f"Intelligence: {neighbour['Intelligence']}",\
                            f"Ambition: {neighbour['Ambition']}", f"Courage: {neighbour['Courage']}", f"Maison: {neighbour['House']}")
                print(f"\nCe personnage se retrouve chez {house}.\n")

        choice = input("Voulez-vous sortir de la boucle ??? (y/n) ")
        while choice != 'n' and choice == 'y':
            choice = input("Voulez-vous sortir de la boucle ??? (y/n) ")
        if choice == 'y':
            running = False

main()
