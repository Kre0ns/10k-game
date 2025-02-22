class Player:

    name = None
    points = 0

    def __init__(self, name):
        self.name = name

    # a function to add points
    def add_points(self, points_to_add):
        self.points += points_to_add
