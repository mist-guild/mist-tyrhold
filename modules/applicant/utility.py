import os
import datetime
import time
from . import applicant_dto
import discord
import requests
import asyncio


def get_applicant_id(channel_name):
    channel_split = channel_name.split("-")
    return channel_split[2]


def build_applicant_from_id(id):
    response = requests.get(os.getenv("APPLICANT_URL") + id)
    applicant = applicant_dto.Applicant(response.json())
    return applicant


def build_applicant_embed(applicant: applicant_dto.Applicant):
    time, date = get_time_and_date()
    color, icon = get_class_color_and_icon(applicant.wow_class)
    embed = discord.Embed(title=f":bookmark_tabs: Application for {applicant.character_name}",
                          description=f"This application was posted at {time} on {date}.", color=color)

    # line break
    embed.add_field(name="\u200B", value="\u200B", inline=False)

    # name/age/bnet
    embed.add_field(name="✍️ Name",
                    value=f"{applicant.character_name}", inline=True)
    embed.add_field(name="🔞 Age",
                    value=f"{applicant.age}", inline=True)
    embed.add_field(name="<:bnet:1035079439014436894> Battle.net",
                    value=f"{applicant.battlenet_contact}", inline=True)

    # line break
    embed.add_field(name="\u200B", value="\u200B", inline=False)

    # discord/class/spec
    embed.add_field(name="<:discord:1035241801541505134> Discord",
                    value=f"{applicant.discord_contact}", inline=True)
    embed.add_field(name=f"{icon} Class",
                    value=f"{applicant.wow_class}", inline=True)
    embed.add_field(
        name="⚔️ Spec", value=f"{applicant.primary_spec}", inline=True)

    # line break
    embed.add_field(name="\u200B", value="\u200B", inline=False)

    # links
    embed.add_field(name="<:wcl:1035242947140141196> WCL",
                    value=f"[Click Here]({applicant.warcraftlogs_link})", inline=True)
    embed.add_field(name="<:rio:1035242933542199376> R.IO",
                    value=f"[Click Here]({applicant.raiderio_link})", inline=True)
    embed.add_field(name="<:wow:1035242960217980978> WCA",
                    value=f"[Click Here]({applicant.armory_link})", inline=True)

    # line break
    embed.add_field(name="\u200B", value="\u200B", inline=False)

    # real life
    embed.add_field(name="📖 Tell us about yourself in real life!",
                    value=f"{applicant.real_life_summary}", inline=False)

    # line break
    embed.add_field(name="\u200B", value="\u200B", inline=False)

    # skills summary
    embed.add_field(name="🎯 What experience, skill, and attitude will you bring to the guild?",
                    value=f"{applicant.skills_summary}", inline=False)

    # line break
    embed.add_field(name="\u200B", value="\u200B", inline=False)

    # procilivity
    embed.add_field(name="🎮 How often do you play WoW?",
                    value=f"{applicant.proclivity_summary}", inline=False)

    # line break
    embed.add_field(name="\u200B", value="\u200B", inline=False)

    # pizza question
    embed.add_field(name="🍕 Does pineapple belong on pizza?",
                    value=f"{applicant.pizza_question}", inline=False)

    # footer
    embed.set_footer(text="Mist Recruiting",
                     icon_url="https://raw.githubusercontent.com/mist-guild/recruitment-manager/master/static/images/mist-icon.png")

    # line break
    embed.add_field(name="\u200B", value="\u200B", inline=False)

    return embed


def get_time_and_date():
    todayVar = datetime.date.today()
    timeVar = time.strftime("%I:%M %p")
    dateVar = todayVar.strftime("%m/%d/%y")
    return timeVar, dateVar


def get_class_color_and_icon(class_name):
    class_colors = {
        "Warrior": 0xC79C6E,
        "Paladin": 0xF58CBA,
        "Hunter": 0xABD473,
        "Rogue": 0xFFF569,
        "Priest": 0xFFFFFF,
        "Death Knight": 0xC41F3B,
        "Shaman": 0x0070DE,
        "Mage": 0x69CCF0,
        "Warlock": 0x9482C9,
        "Monk": 0x00FF96,
        "Druid": 0xFF7D0A,
        "Demon Hunter": 0xA330C9,
        "Evoker": 0x33937F,
    }

    class_icons = {
        "Warrior": '<:Warrior:976616539744792616>',
        "Paladin": '<:Paladin:976616493859078155>',
        "Hunter": '<:Hunter:976616446752874536>',
        "Rogue": '<:Rogue:976616482190528582>',
        "Priest": '<:Priest:976616470391955467>',
        "Death Knight": '<:DeathKnight:976616412288282634>',
        "Shaman": '<:Shaman:976616510183313408> ',
        "Mage": '<:Mage:976616436585881700>',
        "Warlock": '<:Warlock:976616527526768680>',
        "Monk": '<:Monk:976616424699215922> ',
        "Druid": '<:Druid:976616457406390332>',
        "Demon Hunter": '<:DemonHunter:976616398912618517>',
        "Evoker": '<:evoker_flat:1034823772290695259>',
    }

    return class_colors[class_name], class_icons[class_name]
