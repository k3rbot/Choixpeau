from math import sqrt
from csv import DictReader
from random import randint
from browser import document, bind
import csv

amounts = []
with open("question", mode='r', encoding='utf-8') as f:
    question = []
    test_reader = csv.DictReader(f, delimiter=';')
    for element in test_reader:
        for key , value in element.items():
            element[key] = value.split(":")    
            
        amounts = []
        
        for i in element['Amount']:
            amounts.append(i.split(","))
        
        element["Amount"] = amounts
        
        
            
        question.append(element)
print(question)


quizzing = False
qa = [{"Question": "Voulez-vous avancer ?", "Answers": ["Non j'ai trop peur", "Oui je suis un bonhomme", "Pour quoi faire.."], "Values": ["Courage"], "Amount": [[-3], [3], [0]]},
      {"Question": "Partez vous ?", "Answers": ["Oui, il fait froid", "Oui je veux rentrer à temps", "Non", "Oui je ne vous aime pas"], "Values": ["Courage", "Intelligence"], "Amount": [[0, 0.25], [0, 1], [1, -0.25], [2, -1]]}]
qid = 0
profile = {'Intelligence': 0, 'Good': 0, 'Ambition': 0, 'Courage': 0}
nb_q = 2

k = 5

# Création de notre table contenant les personnages et leurs caractéristiques
# à partir de deux fichiers
with open("Characters.csv", mode='r', encoding='utf-8') as f:
        characters_file = DictReader(f, delimiter=';')
        characters_prev = [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in characters_file]

with open("Caracteristiques_des_persos.csv", mode='r', encoding='utf-8') as g:
        characteristics_file = DictReader(g, delimiter=';')
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


def house_of(tab: list, character: dict, k: int=5) -> tuple:
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


def display_qa(event=None):
    global qid
    document["question"].textContent = qa[qid]["Question"]
    for i in range(len(qa[qid]["Answers"])):
        document[str(i)].textContent = qa[qid]["Answers"][i]
        document[str(i)].style.display = "block"
    for i in range(3, len(qa[qid]["Answers"]) -1, -1):
        document[str(i)].style.display = "none"

@bind('#main', 'click')
def start(event):
    global quizzing, qid
    if not quizzing:
        quizzing = True
        document["title"].textContent = "Quizzzzzzzzzzzzzzzzzzzzzzzz"
        document["question"].style.display = "inline-block"
        document["houses_img"].style.display = "none"
        document["main"].textContent = "Menu principal"
        document["main"].style.marginTop = "150px"
        document["main"].style.marginLeft = "25px"
        qid = 0
        display_qa()

    else:
        quizzing = False
        document["title"].textContent = "Un super quizz pour déterminer votre maison Harry Potter !"
        document["houses_img"].style.display = "block"
        document["main"].textContent = "Quizz"
        document["main"].style.marginTop = "30px"
        document["main"].style.marginLeft = "auto"
        for i in range(4):
            document[str(i)].style.display = "none"
        document["question"].style.display = "none"
        document["k"].style.display = 'none'
        document["optimised_k"].style.display = 'none'
        document["k_label"].style.display = 'none'
        document["optimised_k_label"].style.display = 'none'
        document["Hufflepuff.img"].style.display = 'none'
        document["Slytherin.img"].style.display = 'none'
        document["Ravenclaw.img"].style.display = 'none'
        document["Gryffindor.img"].style.display = 'none'


def end_menu():
    document["title"].textContent = "Vos résultats !!!"
    for i in range(4):
        document[str(i)].style.display = "none"
    document["k"].style.display = 'inline'
    document["optimised_k"].style.display = 'inline'
    document["k_label"].style.display = 'inline'
    document["optimised_k_label"].style.display = 'inline'
    house, neighbours = house_of(characters, profile, k)
    document["question"].textContent = "Félicitations, vous êtes :"
    document[house + '_img'].style.display = 'inline-block'


@bind(".answer", 'click')
def answer(event):
    global qid, profile
    for i in range(len(qa[qid]['Values'])):
        profile[qa[qid]['Values'][i]] = qa[qid]['Amount'][int(event.target.id)][i]
    print(profile)
    if qid+1 < nb_q:
        qid += 1
        display_qa()
    else:
        end_menu()

@bind('#k', 'mousemove')
def slider_value(event):
    document["nb_k"].textContent = document['k'].value
