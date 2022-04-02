from glob import glob
from math import sqrt
from random import randint
from browser import document

quizzing = False
qa = [{"Question": "Voulez-vous avancer ?", "Answers": ["Non j'ai trop peur", "Oui je suis un bonhomme", "Pour quoi faire.."], "Values": ["Courage"], "Amount": [[-3], [3], [0]]},
      {"Question": "Partez vous ?", "Answers": ["Oui, il fait froid", "Oui je veux rentrer à temps", "Non", "Non je ne vous aime pas"], "Values": ["Courage", "Intelligence"], "Amount": [[0, 0.25], [0, 1], [1, -0.25], [2, -1]]}]
qid = 0

def display_qa(event=None):
    global qid
    document["question"].textContent = qa[qid]["Question"]
    for i in range(len(qa[qid]["Answers"])):
        document[str(i+1)].textContent = qa[qid]["Answers"][i]
        document[str(i+1)].style.display = "block"
    for i in range(4, len(qa[qid]["Answers"]), -1):
        document[str(i)].style.display = "none"
    qid += 1


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
            document[str(i+1)].style.display = "none"
        document["question"].style.display = "none"


def answer(event):
    console.log(event)

document["main"].bind("click", start)
document["answer"].bind("click", answer)
