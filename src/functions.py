from random import SystemRandom
from collections import Counter


# returns a list of dice rolls
def dice_rolls(num_rolls):
    rolls = []

    for i in range(num_rolls):
        rolls.append(SystemRandom().randint(1, 6))

    return [1, 5, 3, 4, 6, 2]


# replaces all 1's in a list with 10's (needed for point logic)
def one_to_ten(raw_rolls):
    parsed_rolls = []

    for item in raw_rolls:
        if item == 1:
            parsed_rolls.append(10)

        else:
            parsed_rolls.append(item)

    return parsed_rolls


# calculates the points from a list of rolls provided
def points_calc(raw_rolls):
    parsed_rolls = one_to_ten(raw_rolls)

    roll_frequencies = Counter(parsed_rolls)
    frequency_values = list(roll_frequencies.values())

    points = 0

    if sorted(parsed_rolls) == [2, 3, 4, 5, 6, 10]:
        points += 1500

    elif frequency_values.count(3) == 2:
        points += 2500

    elif frequency_values.count(2) == 3:
        points += 1500

    else:
        for roll in roll_frequencies:
            if roll_frequencies[roll] == 3:
                points += roll * 100

            elif roll_frequencies[roll] == 4:
                points += 2 * (roll * 100)

            elif roll_frequencies[roll] == 5:
                points += 3 * (roll * 100)

            elif roll_frequencies[roll] == 6:
                points += 4 * (roll * 100)

            elif roll == 10 or roll == 5:
                points += (roll * 10) * roll_frequencies[roll]

    return points


# compares the scores to find the highest score and returns the player with it
def find_winner(player_list):
    best_score = 0
    winner = None

    for player in player_list:
        if player.points > best_score:
            best_score = player.points
            winner = player

    return winner
