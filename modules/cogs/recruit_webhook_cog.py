import os
from discord import webhook
from discord.ext import commands
from ..services import recruit_webhook_service


class RecruitWebhookCog(commands.Cog, name="Recruit Webhook"):
    """Mist Bot's interaction with the Recruit Webhook"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user:
            return

        if message.author.id == int(os.getenv("RECRUIT_WEBHOOK_ID")):
            embed = message.embeds[0]
            channel_name = utility.get_channel_name(
                embed.author.name, embed.title[20:])
            channel = await utility.create_text_channel(self.bot, channel_name)
            embed.url = channel.jump_url
            await message.delete()
            await message.channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitWebhookCog(bot))
