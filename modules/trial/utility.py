import os
from . import applicant_dto
import discord
import requests

def get_applicant_id(channel_name):
    channel_split = channel_name.split("-")
    return channel_split[2]

def build_applicant_from_id(id):
    response = requests.get(os.getenv("APPLICANT_URL") + id)
    applicant = applicant_dto.Applicant(response)
    return applicant


class TrialUtility:

    @staticmethod
    def get_new_trial_embed(name: str, id: int):
        embed = discord.Embed()
        url = os.getenv("APPLICANT_URL")
        embed.description = f"[{name}'s Application]({url}/{id})"
        return embed

    @staticmethod
    def get_trial_syntax_error_embed():
        embed = discord.Embed()
        embed.description = "Incorrect syntax! Please follow this skeleton: !mb trial <name> <id>"
        return embed
