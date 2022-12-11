import os
from modules.utility.discord_utility import DiscordUtility


class RecruitWebhookService:
    @staticmethod
    async def generate_recruit_text_channel(guild, author_string, team_name):
        # get name/id
        author_split = author_string.split("•")
        name = author_split[0].strip()
        name = name.split("-")[0] if "-" in name else name
        id = author_split[1].strip()

        # get team name
        team_name = "wb" if team_name == "Windbridge" else "cc"

        # create channel
        channel_name = f"{team_name}-{name}-{id}"
        category = DiscordUtility.get_category_by_id(
            guild, int(os.getenv("RECRUIT_CATEGORY_ID")))
        new_channel = await DiscordUtility.create_text_channel(
            guild, channel_name, category)

        # return channel
        return new_channel
