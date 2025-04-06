import random

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

questions = [
    {
        "text" : "Какой язык программивания используется для Flask",
        "options": ["JavaScript", "Python", "HTML" , "CSS"],
        "answer" : "Python"
    },
    {
        "text": "Какой порт используется для запуска?",
        "options": ["5000", "200", "404", "3999"],
        "answer": "5000"
    },
    {    #ключ : значение
        "text": "Код состояния 404:",
        "options": ["Все хорошо", "Все очень хорошо", "Интернета нету", "Страница не найдена"],
        "answer": "Страница не найдена"
    },
]
current_question = 0 #номер текущего вопроса
score = 0  #счет


@app.route('/')
def home():
    return render_template("index.html")

#GET - показывает вопросы, POST - получает ответы
@app.route('/quizz' , methods=["GET" , "POST"])
def quizz():
    global  current_question, score
    if request.method == "POST":
        user_answer = request.form.get("answer") #получает ответ от пользователя
        if user_answer == questions[current_question]["answer"]:
            score = score + 1
        current_question = current_question + 1
        if current_question >= len(questions):
            return redirect(url_for("result"))
        else:
            return redirect(url_for("quizz"))

    return render_template("quizz.html", question = questions[current_question])

@app.route('/result')
def result():
    return render_template("result.html", score=score, total=len(questions))

#---------- Забавные истории
stories = [
    "Однажды {name} купил(а) {item} и решил(а) отнести его в {place}. Но там произошло нечто удивительное!",
    "{name} отправился(ась) в путешествие в {place}, но по дороге обнаружил(а) {item}. Это стало началом приключений!",
    "Как-то раз {name} решил пойти {place} один раз в жизни, но его поймали и забрали у него {item}",
    "В один день {name} нашел {item} и это изменило его жизнь. Что он улетел {place}",
]
@app.route('/story' , methods=["GET" , "POST"])
def history():
    story = None
    if request.method == 'POST':
        name = request.form.get('name')
        place = request.form.get('place')
        item = request.form.get('item')

        if name and place and item:
            chosen_story = random.choice(stories)
            story = chosen_story.format(name=name, place=place, item=item)
        else:
            story = "Заполните все поля"
    return render_template("story.html", story=story)




if __name__ == '__main__':
    app.run(debug=True)