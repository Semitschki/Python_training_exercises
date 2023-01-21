"""Add Module to calculate sides, area and circumference from a polygon."""

import math


def get_length(point_1, point_2):
    """Function to calculate the length of 2 points."""
    (x_1, y_1) = point_1
    (x_2, y_2) = point_2
    x_difference = x_2 - x_1
    y_difference = y_2 - y_1
    return math.sqrt(x_difference**2 + y_difference**2)


class Polygon:
    """Class to calculate the size of the area and the length of the sides."""
    def __init__(self, points):
        if len(points) < 3:
            raise ValueError("Cannot be a polygon!")
        self.points = points

    def area(self):
        """Method to calculate the size of the area."""
        area = 0
        for (idx, (x_1, y_1)) in enumerate(self.points[:-1]):
            (x_2, y_2) = self.points[idx+1]
            area += x_1 * y_2 - y_1 * x_2
        area += (
            (self.points[-1][0] * self.points[0][1]) -
            (self.points[-1][1] * self.points[0][0])
        )
        return abs(0.5 * area)

    def get_sides(self, rounded=2):
        """Method to calculate the length of the sides."""
        all_sides = []
        for (idx, point) in enumerate(self.points[:-1]):
            all_sides.append((
                ((point, self.points[idx+1])),
                round(get_length(point, self.points[idx + 1]), rounded)
            ))
        all_sides.append((
            ((self.points[-1], self.points[0])),
            round(get_length(self.points[-1], self.points[0]), rounded)
        ))
        return tuple(all_sides)

    def circumference(self):
        """Method to calculate the circumference."""
        side_length = self.get_sides()
        return round(sum(point[-1] for point in side_length), 2)

