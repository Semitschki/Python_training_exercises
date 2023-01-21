"""Module to calculate geometric attributes"""

import copy
import math

from polygon import Polygon


def cal_angle(cathete_1, cathete_2, hypotenuse):
    """Calculates the angle between the two catheters."""
    numerator = cathete_1**2 + cathete_2**2 - hypotenuse**2
    denominator = 2 * cathete_1 * cathete_2

    cathete_angle = math.degrees(math.acos(numerator / denominator))

    return cathete_angle


class Triangle(Polygon):
    """Class to calculate the angles and to determine the type of the triangle."""
    def __init__(self, *args):
        super().__init__(args)
        if len(args) != 3:
            raise ValueError("Cannot be a triangle")

    def get_angles(self):
        """Method to calculate the angle of a triangle."""
        calculated_sides = self.get_sides(rounded=6)
        lengths = [point[-1] for point in calculated_sides]
        a_angle = round(cal_angle(lengths[1], lengths[2], lengths[0]), 3)
        c_angle = round(cal_angle(lengths[0], lengths[2], lengths[1]), 3)
        b_angle = round(180 - (c_angle + a_angle), 3)
        return (
            (self.points[0], c_angle),
            (self.points[1], b_angle),
            (self.points[2], a_angle)
        )

    #pylint: disable=too-many-locals
    def get_circumcenter_center(self):
        """Method to calculate the circumcenter of a triangle."""
        (point_1x, point_1y) = (self.points[0][0], self.points[0][1])
        (point_2x, point_2y) = (self.points[1][0], self.points[1][1])
        (point_3x, point_3y) = (self.points[2][0], self.points[2][1])
        number_a = -((point_2x - point_3x) / (point_2y - point_3y))
        number_b = -((point_1x - point_3x) / (point_1y - point_3y))
        numerator = 1 / (2 * (number_a - number_b))
        denominator_1 = ((point_1x**2 - point_3x**2)
                         / (point_1y - point_3y))
        denominator_2 = -((point_2x**2 - point_3x**2)
                          / (point_2y - point_3y))
        subtract = (point_1y - point_2y)
        x_number = round(numerator * (denominator_1 + denominator_2 + subtract), 2)
        y_number = 0.5 * (number_a * (2 * x_number - point_1x - point_3x)
                          + point_1y + point_3y)
        return (x_number, y_number)

    def get_circumcenter_circle(self):
        """Methode to create the circumference of a triangle."""
        point = self.get_circumcenter_center()
        radius = round(
            math.sqrt(
                ((self.points[0][0] - point[0])**2)
                +((self.points[0][1] - point[1])**2)
            ), 3)
        return Circle(point, radius)

    #pylint: disable=inconsistent-return-statements
    def get_type(self, option):
        """Method to determine the type of the triangle."""
        if option == "side":
            check_sides = set(round(side[-1], 2) for side in self.get_sides())
            _map = {
                1: "obtuse",
                2: "isosceles",
                3: "irregular",
            }
            return _map[len(check_sides)]

        if option == "angle":
            angles = self.get_angles()
            angles = tuple(round(angle[-1], 2) for angle in angles)
            if any(angle > 90 for angle in angles):
                return "obtusely"
            if 90 in angles:
                return "right_angled"
            return "acute"
        raise ValueError("Enter a option: angle or side!")


class Quadrilateral(Polygon):
    """Class to calculate the angles and to determine the type of the quadrilateral object."""
    def __init__(self, *args):
        super().__init__(args)
        if len(args) != 4:
            raise ValueError("Cannot be a Quadrilateral!")

    def get_diagonal(self):
        """Method to calculate the diagonal of two sides."""
        points = list(self.points)
        self.points = points[:-1]
        diagonal = self.get_sides(rounded=6)
        diagonal = diagonal[-1][-1]

        self.points = points[1:]
        diagonal_2 = self.get_sides(rounded=6)
        diagonal_2 = diagonal_2[-1][-1]
        self.points = points
        return (diagonal, diagonal_2)

    def get_angles(self):
        """Method to calculate the angle of a quadrilateral object."""
        cal_sides = self.get_sides(rounded=6)
        (diagonal, diagonal_2) = self.get_diagonal()
        sides = [length[-1] for length in cal_sides]
        a_angle = round(cal_angle(sides[1], sides[0], diagonal), 3)
        b_angle = round(cal_angle(sides[2], sides[1], diagonal_2), 3)
        c_angle = round(cal_angle(sides[3], sides[2], diagonal), 3)
        d_angle = round(360 - (a_angle + c_angle + b_angle), 3)
        return (
            (self.points[0], b_angle),
            (self.points[1], a_angle),
            (self.points[2], d_angle),
            (self.points[3], c_angle)
        )

    def get_type(self):
        """Method to determine the type of the quadrilateral object."""
        square_angles = self.get_angles()
        sides = self.get_sides()
        angles = [angle for angle in square_angles]
        check_sides = set(side[-1] for side in sides)
        if len(check_sides) == 1 and all(angle[-1] == 90 for angle in square_angles):
            return "square"
        if all(angle[-1] == 90 for angle in square_angles):
            return "rectangle"
        if (angles[0][1] == angles[2][1]) and (angles[1][1] == angles[-1][1]):
            return "rhombus"
        return "trapezium"


class Pentagon(Polygon):
    """Class to calculate the angles and to determine the type of a Pentagon."""
    def __init__(self, *args):
        super().__init__(args)
        if len(args) != 5:
            raise ValueError("Cannot be a Pentagon!")
        self.points_2 = copy.deepcopy(self.points)

    def get_diagonal(self):
        """Method to calculate the diagonal of two sides."""
        points = tuple(self.points)
        self.points = points[0:3]
        diagonal_1 = self.get_sides(rounded=6)[-1][-1]
        self.points = points[1:4]
        diagonal_2 = self.get_sides(rounded=6)[-1][-1]
        self.points = points[2:5]
        diagonal_3 = self.get_sides(rounded=6)[-1][-1]
        self.points = points[3], points[4], points[0]
        diagonal_4 = self.get_sides(rounded=6)[-1][-1]
        self.points = points
        return (diagonal_1, diagonal_2, diagonal_3, diagonal_4)

    def get_angles(self):
        """Method to calculate the angle of a pentagon."""
        cal_sides = self.get_sides(rounded=6)
        (diagonal_1, diagonal_2, diagonal_3, diagonal_4) = self.get_diagonal()
        sides = [length[-1] for length in cal_sides]
        a_angle = round(cal_angle(sides[1], sides[0], diagonal_1), 3)
        b_angle = round(cal_angle(sides[2], sides[1], diagonal_2), 3)
        c_angle = round(cal_angle(sides[3], sides[2], diagonal_3), 3)
        d_angle = round(cal_angle(sides[4], sides[3], diagonal_4), 3)
        e_angle = round(540 - (a_angle + b_angle + c_angle + d_angle), 3)
        return (
            (self.points_2[0], e_angle),
            (self.points_2[1], a_angle),
            (self.points_2[2], b_angle),
            (self.points_2[3], c_angle),
            (self.points_2[4], d_angle)
        )

    #pylint: disable=no-else-return
    def get_type(self):
        """Method to determine the type of the Pentagon."""
        pentagon_angle = self.get_angles()
        if any(angle[-1] >= 180 for angle in pentagon_angle):
            return "concave"
        else:
            return "convex"
        raise ValueError("Cannot be a Pentagon")


class Circle:
    """Class to calculate the area and cicumference of a circle."""
    def __init__(self, point, radius):
        if radius > 0:
            self.points = point
            self.radius = radius
        else:
            raise ValueError("radius cannot be zero or smaller!")

    def get_area(self):
        """Method to calculate the area of a circle."""
        return round((math.pi * self.radius**2), 2)

    def get_circumference(self):
        """Method to calculate the circumference of a circle."""
        return round((2 * math.pi * self.radius), 2)

