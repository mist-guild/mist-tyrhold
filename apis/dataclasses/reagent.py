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
        if response.status_code == 404:
            return None
        reagent = Reagent(response.json())
        return reagent
