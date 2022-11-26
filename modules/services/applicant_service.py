import os
import discord
import base64
import zlib
import json
from apis.valdrakken import Valdrakken
from modules.dataclasses.applicant import Applicant
from modules.utility.general_utility import GeneralUtility
from modules.utility.discord_utility import DiscordUtility


def build_applicant_embed(channel_name):
    # get ID from channel name
    id = DiscordUtility.get_applicant_id_from_channel_name(channel_name)

    # build applicant from ID
    applicant = Applicant.build_applicant_from_id(id)

    # build embed
    time, date = GeneralUtility.get_time_and_date()
    color, icon = GeneralUtility.get_class_color_and_icon(applicant.wow_class)
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

    return embed, applicant


def get_previous_applications(applicant):
    data = {"discord_contact": applicant.discord_contact,
            "battlenet_contact": applicant.battlenet_contact,
            "called_from": applicant.id}

    response = Valdrakken.get("/applicant/exists/",
                              content=json.dumps(data))
    return response.json()


async def archive_comments(channel):
    # get id
    id = DiscordUtility.get_applicant_id_from_channel_name(channel.name)

    # archive channel messages into compressed string
    archived_messages = ""
    current_author = None
    async for message in channel.history(oldest_first=True, limit=None):
        if message.author.id == int(os.getenv("BOT_ID")):
            continue
        if current_author == None:
            current_author = message.author
            archived_messages += f"\n**{message.author}**\n"
        if current_author != message.author:
            current_author = message.author
            archived_messages += f"\n**{message.author}**\n"
        archived_messages += f"{message.content}\n"
    encoded_messages = base64.b64encode(
        zlib.compress(archived_messages.encode()))

    # send to valdrakken to append to DB
    Valdrakken.put(f"/applicant/archive/{id}/",
                   content=encoded_messages,
                   content_type='application/octet-stream')


async def create_text_channel(guild, channel_name):
    # get guild and category
    category_id = int(os.getenv("RECRUIT_CATEGORY_ID"))
    category = discord.utils.get(guild.categories, id=category_id)

    # create and return channel
    print("epic")
    channel = await guild.create_text_channel(name=channel_name, category=category)
    return channel


def get_archive_channel_name(applicant):
    team_name = "wb" if applicant.team_choice == "Windbridge" else "cc"
    return f"archive-{applicant.id}-{team_name}"
