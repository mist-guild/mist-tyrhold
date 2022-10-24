import os
import discord


class TrialUtility:

    @staticmethod
    def get_trial_channel_name(name: str, id: int):
        return f"{name}-{id}"

    @staticmethod
    async def create_new_trial_channel(called_from, guild, channel_name):
        if called_from == int(os.getenv('WB_APP_CHANNEL')):
            category_id = int(os.getenv('WB_APP_CATEGORY'))
        else:
            category_id = int(os.getenv('CC_APP_CATEGORY'))
        category = discord.utils.get(guild.categories, id=category_id)
        channel = await guild.create_text_channel(name=channel_name, category=category)
        return channel

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
