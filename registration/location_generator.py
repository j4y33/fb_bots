import random
from config.config import config


class LocationGenerator:
    @classmethod
    def get_university(cls):
        with open(config.universities) as universities_file:
            universities = universities_file.read().splitlines()
        return random.choice(universities)

    @classmethod
    def get_city_and_school(cls):
        with open(config.cities_and_schools) as cities_and_schools_file:
            cities_and_schools = cities_and_schools_file.read().splitlines()
        return random.choice(cities_and_schools)
