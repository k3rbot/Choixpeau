from math import sqrt
from random import randint
from browser import document, bind

quizzing = False
qa = [{"Question": "Voulez-vous avancer ?", "Answers": ["Non j'ai trop peur", "Oui je suis un bonhomme", "Pour quoi faire.."], "Values": ["Courage"], "Amount": [[-3], [3], [0]]},
      {"Question": "Partez vous ?", "Answers": ["Oui, il fait froid", "Oui je veux rentrer à temps", "Non", "Oui je ne vous aime pas"], "Values": ["Courage", "Intelligence"], "Amount": [[0, 0.25], [0, 1], [1, -0.25], [2, -1]]}]
qid = 0
profile = {'Intelligence': 0, 'Good': 0, 'Ambition': 0, 'Courage': 0}
nb_q = 2

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

def end_menu():
    document["title"].textContent = "Vos résultats !!!"
    document["houses_img"].style.display = "block"
    for i in range(4):
        document[str(i)].style.display = "none"
    document["question"].style.display = "none"

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
