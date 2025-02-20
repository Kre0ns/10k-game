import random


def dice_rolls(num_rolls):
    rolls = []

    for i in range(num_rolls):
        rolls.append(random.randint(1, 6))

    return rolls
