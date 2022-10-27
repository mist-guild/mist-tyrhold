import os
from discord.ext import commands
from . import utility


class RecruitWebhookCog(commands.Cog, name="Recruit Webhook"):
    """Mist Bot's interaction with the Recruit Webhook"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user:
            return

        # TODO: change this to mist cc webhook id
        if message.author.id == 1026049033439023155:
            embed = message.embeds[0]
            channel_name = utility.get_channel_name(
                embed.author.name, embed.title[20:])
            await utility.create_text_channel(self.bot, channel_name)


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitWebhookCog(bot))
