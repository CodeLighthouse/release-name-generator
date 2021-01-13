import os
from typing import List
import random


def name_generator():
    bank = prepare_bank_list()

    adjective = random.sample(bank["adjectives"], 1)[0]
    lizard = random.sample(bank["lizards"], 1)[0]

    print(f"{adjective} {lizard}")


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

if __name__ == "__main__":
    name_generator()