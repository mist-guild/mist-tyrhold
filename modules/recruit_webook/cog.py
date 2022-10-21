import os
from discord.ext import commands


class RecruitWebhookCog(commands.Cog, name="Recruit Webhook"):
    """Mist Bot's interaction with the Recruit Webhook"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user:
            return

        if message.author.id == int(os.getenv("WEBHOOK_ID")):
            emojis = ["👍", "👎", "💬"]
            for emoji in emojis:
                await message.add_reaction(emoji)


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitWebhookCog(bot))
