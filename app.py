from flask import Flask, render_template, request
import random
import pandas as pd

app = Flask(__name__)

df = pd.read_excel('df.xlsx', header=None, engine='openpyxl')

english_german = {row[1]: row[0] for _, row in df.iterrows()}


def find_matching_word(word, lang):
    if lang == "en":
        return english_german[word]
    else:
        for key, value in english_german.items():
            if value == word:
                return key


app.jinja_env.globals.update(find_matching_word=find_matching_word)


@app.template_filter('enumerate')
def _enumerate(iterable):
    return enumerate(iterable)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        size = int(request.form.get("size"))
        pexeso_data = generate_pexeso_data(size)
        return render_template("game.html", size=size, data=pexeso_data)
    return render_template("index.html")


def generate_pexeso_data(size):
    words = list(english_german.items())
    random.shuffle(words)
    words = words[:size * size // 2]
    pexeso_data = []
    for index, (eng, ger) in enumerate(words):
        pexeso_data.append((eng, "en", index))
        pexeso_data.append((ger, "de", index))
    random.shuffle(pexeso_data)
    return pexeso_data


if __name__ == "__main__":
    app.run(debug=True)
