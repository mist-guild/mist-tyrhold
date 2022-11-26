import os
from discord.ext import commands
from modules.services.recruit_webhook_service import RecruitWebhookService


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
            new_channel = RecruitWebhookService.generate_recruit_text_channel(
                message.guild, embed.author.name, embed.title[20:])
            embed.url = new_channel.jump_url
            await message.delete()
            await message.channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitWebhookCog(bot))
