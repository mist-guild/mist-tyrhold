import zlib
import base64
from dataclasses import dataclass


@dataclass
class Applicant:
    age: int
    armory_link: str
    battlenet_contact: str
    character_name: str
    discord_contact: str
    id: int
    pizza_question: str
    primary_spec: str
    proclivity_summary: str
    raiderio_link: str
    real_life_summary: str
    skills_summary: str
    team_choice: str
    warcraftlogs_link: str
    wow_class: str
    archived_comments: str

    def __init__(self, response):
        for key in response:
            setattr(self, key, response[key])

    def decode_archived_comments(self):
        return zlib.decompress(
            base64.b64decode(
                bytes(self.archived_comments, encoding='utf-8')
            )
        ).decode()
