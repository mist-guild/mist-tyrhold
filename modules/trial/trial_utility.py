import discord


class TrialUtility:

    @staticmethod
    def get_trial_channel_name(name: str, id: int):
        return f"{name}-{id}"

    @staticmethod
    async def create_new_trial_channel(guild, channel_name):
        category = discord.utils.get(guild.categories, id=1032096448784912385)
        channel = await guild.create_text_channel(name=channel_name, category=category)
        return channel

    @staticmethod
    def get_new_trial_embed(name: str, id: int):
        embed = discord.Embed()
        embed.description = f"[{name}'s Application](https://mistguild.pythonanywhere.com/applicant/{id})"
        return embed
