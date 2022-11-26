import os
import discord


def get_channel_name(author_string, team_name):
    # seperate name and id
    author_split = author_string.split("•")
    name = author_split[0].strip()
    name = parse_chracter_name(name)
    id = author_split[1].strip()

    # abbreviate team
    team_name = "wb" if team_name == "Windbridge" else "cc"

    # return channel name
    return f"{team_name}-{name}-{id}"


async def create_text_channel(bot, channel_name):
    # get guild and category
    guild = bot.get_guild(int(os.getenv("MIST_GUILD_ID")))
    category_id = int(os.getenv("RECRUIT_CATEGORY_ID"))
    category = discord.utils.get(guild.categories, id=category_id)

    # create and return channel
    channel = await guild.create_text_channel(name=channel_name, category=category)
    return channel


def parse_chracter_name(name):
    if '-' in name:
        return name.split("-")[0]
    return name
