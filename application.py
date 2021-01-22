import os
from typing import List
import random
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")


def prepare_bank_list():
    bank = _tunnel("./banks")

    word_bank = {}

    for file_path in bank:
        file_name = get_file_name(file_path)
        word_bank[file_name] = set()
        with open(f"./banks{file_path}", "r") as f:
            while True:
                word = f.readline()
                if not word:
                    break
                word = word[:-1]  # REMOVE THE \n AT THE END OF THE WORD
                word_bank[file_name].add(word)

    return word_bank


def _tunnel(path: str, prepend: str = "") -> List[str]:
    bank = []
    for item in os.listdir(path):
        if "." in item:
            # IF A FILE TYPE (TXT)
            bank.append(f"{prepend}/{item}")
        else:
            # IF A DIRECTORY, CONTINUE DOWN AND PREPEND THE DIRECTORY NAME
            bank += _tunnel(f"{path}/{item}", f"{prepend}/{item}")
    return bank


def get_file_name(file_path):
    file_path = file_path.split(".")[0]
    return file_path.split("/")[-1]


BANK = prepare_bank_list()


@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html.jinja2")


@app.route("/", methods=["POST"])
def name_generator():
    category_1 = request.form.get("category_1", "adjectives")
    category_2 = request.form.get("category_2", "lizards")

    word_1 = random.sample(BANK[category_1], 1)[0]
    word_2 = random.sample(BANK[category_2], 1)[0]

    name = f"{word_1} {word_2}"

    return render_template("index.html.jinja2", name=name)


if __name__ == "__main__":
    app.run()
