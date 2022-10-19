import discord

class TrialUtility:
    @staticmethod
    def get_trial_channel_name(name: str, id: int):
        return f"{name}-{id}" 
    
    @staticmethod
    async def create_new_trial_channel(guild, channel_name):
        category = discord.utils.get(guild.categories, id=1032096448784912385)
        await guild.create_text_channel(name=channel_name, category=category)