import os
import json


def load_words():
    if not os.path.exists(out_file):
        return []
    return json.load(open(out_file))


out_file = "words.json"
