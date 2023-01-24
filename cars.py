"""Add modul to create a car from a csv and json config."""

import csv
import json

NOT_AVAILABLE = "This model is not available."
NOT_AVAILABLE_BRAND = "This model is not available for the brand."
MODELS = ["1 Series", "3 Series", "4 Series", "5 Series", "7 Series"]


def _iter_rows_csv(path):
    """Function to iterate over a csv file."""
    with open(path, encoding="Latin1") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quoting=csv.QUOTE_NONE)
        yield from reader


class CarDealer:
    """Class to create the config for the car class."""
    def __init__(self, brand):
        self.brand = brand

    def build_vehicle(self, config):
        """Create the car config from a dict."""
        brand = self.brand
        model = config["model"]
        engine = config["engine"]
        colour = config["colour"]
        return Car(brand, model, colour, engine)

    def build_from_csv(self, path, model):
        """Create the car config from csv file."""
        if model in MODELS:
            for row in _iter_rows_csv(path):
                if model in row:
                    csv_list = row
        else:
            raise ValueError(NOT_AVAILABLE)
        brand = csv_list[0]
        model = csv_list[1]
        engine = float(csv_list[2])
        colour = csv_list[3]
        if self.brand != brand:
            raise ValueError(NOT_AVAILABLE_BRAND)
        return Car(brand, model, colour, engine)

    #pylint:disable=inconsistent-return-statements
    def build_from_json(self, path, model):
        """Create the car config from json file."""
        with open(path) as output_file:
            output_json = json.load(output_file)
        if model not in MODELS:
            raise ValueError(NOT_AVAILABLE)
        cars = output_json["cars"]
        for car in cars:
            if car and (model == car["model"]):
                if self.brand != car["brand"]:
                    raise ValueError(NOT_AVAILABLE_BRAND)
                return Car(**car)


class Car:
    """Class to create a Car."""
    #pylint:disable=too-many-arguments
    def __init__(self, brand, model, colour, engine, engine_started=False):
        if model not in MODELS:
            raise ValueError(NOT_AVAILABLE)
        self.brand = brand
        self.mileage = 0
        self.model = model
        self.colour = colour
        self.engine = engine
        self.engine_started = engine_started

    def start_engine(self):
        """Method to start the car."""
        if not self.engine_started:
            self.engine_started = True
            print("BRUMMMMM...",)
        else:
            print("Engine is already running.")

    def drive(self, destination, distance):
        """Mehtod to drive the car."""
        if self.engine_started:
            self.mileage += distance
            return ("car drive to:", destination, "mileage of the car is:", distance)
        return "Engine is turnt off"

    #pylint:disable=no-self-use
    def honk(self):
        """Method to print Tutuuut."""
        print("Tutuuut")
