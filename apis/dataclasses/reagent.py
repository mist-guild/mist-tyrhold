from dataclasses import dataclass
from apis.valdrakken import Valdrakken


@dataclass
class Reagent:
    id: int
    character_name: str
    hochenblume_bronze: int
    writhebark_gold: int
    bubble_poppy_bronze: int
    bubble_poppy_silver: int

    def __init__(self, response):
        for key in response:
            setattr(self, key, response[key])

    @staticmethod
    def build_reagent_from_character_name(character_name):
        response = Valdrakken.get(f"/reagent/{character_name}")
        reagent = Reagent(response.json())
        return reagent
