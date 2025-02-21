from random import SystemRandom
from collections import Counter


def dice_rolls(num_rolls):
    rolls = []

    for i in range(num_rolls):
        rolls.append(SystemRandom().randint(1, 6))

    return rolls


def one_to_ten(list_rolls):
    new_list = []
    for item in list_rolls:
        if item == 1:
            new_list.append(10)
        else:
            new_list.append(item)
    return new_list


def points_calc(unsorted_rolls):
    list_rolls = one_to_ten(unsorted_rolls)
    counter_dict_rolls = Counter(list_rolls)
    points = 0
    num_list_values = list(counter_dict_rolls.values())

    if sorted(list_rolls) == [1, 2, 3, 4, 5, 6]:
        points += 1500
    elif num_list_values.count(3) == 2:
        points += 2500
    elif num_list_values.count(2) == 3:
        points += 1500
    else:
        for roll in counter_dict_rolls:
            if counter_dict_rolls[roll] == 3:
                points += roll * 100
            elif counter_dict_rolls[roll] == 4:
                points += 2 * (roll * 100)
            elif counter_dict_rolls[roll] == 5:
                points += 3 * (roll * 100)
            elif counter_dict_rolls[roll] == 6:
                points += 4 * (roll * 100)
            elif roll == 10 or roll == 5:
                points += (roll * 10) * counter_dict_rolls[roll]
    return points
