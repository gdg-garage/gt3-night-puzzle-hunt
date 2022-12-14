import json
import random
import re

from lib import load_words, out_file

limit = 3 * 42


def words():
    with open("cs_CZ.dic") as f:
        for line in f:
            yield line.strip().split('/')[0]


def is_word_good(w: str):
    # upper means names and surnames (we do not need that)
    return re.match(r"^(?![xw])[a-z]{5}$", w)


def main():
    wordlist = list(set((w for w in words() if is_word_good(w))))
    print(f"words: {len(wordlist)}")
    chosen = set(load_words())

    while len(chosen) < limit:
        word = random.choice(wordlist)
        print(word)
        good = input("Good? (y/n)").lower()
        if good == 'y':
            chosen.add(word)
            json.dump(list(chosen), open(out_file, "w"))
            print(f"added ({len(chosen)}/{limit})")
    print(chosen)


if __name__ == '__main__':
    main()
