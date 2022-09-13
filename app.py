import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        mood = request.form["mood"]
        language = request.form["language"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(mood, language),
            temperature=0.6,
            max_tokens=256
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    if result:
        result=result.splitlines()
    return render_template("index.html", result=result)


def generate_prompt(mood, language):
    return """Suggest three quotes that reflect the given mood.

Mood: Happy
Language: English
Quotes: "The greatest happiness you can have is knowing that you do not necessarily require happiness." 
- William Saroyan 
"The greatest happiness of life is the conviction that we are loved; loved for ourselves, or rather, loved in spite of ourselves." 
- Victor Hugo 
"Happiness is not something ready made. It comes from your own actions." 
- Dalai Lama
Mood: Sad
Language: English
Quotes: "The greatest pain that comes from love, is loving someone you can never have." 
- Unknown
"I'm not crying because of you; you're not worth it. I'm crying because my delusion of who you were was so much better than who you really are." 
- Unknown
"It's better to have loved and lost, than to have never loved at all." 
- Alfred Lord Tennyson
Mood: Jealous
Language: French
"La jalousie est un sentiment absurde, puisque c'est nous qui créons les circonstances qui nous rendent jaloux." 
- Paulo Coelho 
"La jalousie c'est l'amour sans les ailes." 
- Victor Hugo 
"La jalousie est une maladie qui mange le corps, épuise le cerveau et détruit l'âme." 
- Proverbe arabe
Mood: {}
Language: {}
Quotes:""".format(
        mood.capitalize(),
        language.capitalize()
    )
