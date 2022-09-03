
import random

people = [
        "Simon",
        "Alena",
        "Otas",
        "Tomas M.",
        "David",
        "Adrian",
        "Honza H.",
        "Kuba S.",
        # "Kata",
        "Harry",
        # "Honza S.",
        "Andrej",
        "Fisa",
        # "Long",
        "Rasto",
        "Tadeas B.",
        "Ales F.",
        "Martin T.",
        "Tomas L.",
        # "Martin Ch.",
        # "Tadeas U.",
        # "Honza N.",
        "Ales Z.",
        "Petr V.",
        ]
group_size = 2
group_nr = 0
while people:
    group_nr += 1
    group = []
    for i in range(group_size):
        if not people:
            break
        idx = random.randrange(0, len(people))
        group.append(people.pop(idx))
    print(f"Team {group_nr}: {group}")

