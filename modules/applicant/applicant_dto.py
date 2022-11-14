import zlib
import base64


class Applicant:
    def __init__(self, response):
        self.age = response["age"]
        self.armory_link = response["armory_link"]
        self.battlenet_contact = response["battlenet_contact"]
        self.character_name = response["character_name"]
        self.discord_contact = response["discord_contact"]
        self.id = response["id"]
        self.pizza_question = response["pizza_question"]
        self.primary_spec = response["primary_spec"]
        self.proclivity_summary = response["proclivity_summary"]
        self.raiderio_link = response["raiderio_link"]
        self.real_life_summary = response["real_life_summary"]
        self.skills_summary = response["skills_summary"]
        self.team_choice = response["team_choice"]
        self.warcraftlogs_link = response["warcraftlogs_link"]
        self.wow_class = response["wow_class"]
        self.archived_comments = response["archived_comments"]

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def to_json(self):
        return self.wow_class

    def decode_archived_comments(self):
        return zlib.decompress(
            base64.b64decode(
                bytes(self.archived_comments, encoding='utf-8')
            )
        ).decode()
