import os
import re
from discord.ext import commands
from . import utility


class ApplicantCog(commands.Cog, name="Applicant"):
    """Mist Bot's interaction with applicants and the trialing process"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.category_id != int(os.getenv("RECRUIT_CATEGORY_ID")):
            return

        id = utility.get_applicant_id(channel.name)
        applicant = utility.build_applicant_from_id(id)
        embed = utility.build_applicant_embed(applicant)
        message = await channel.send(embed=embed)
        await message.pin()

    @commands.command("end")
    async def end(self, ctx: commands.Context):
        """Deletes an applicant text channel"""
        if re.match('.{2}-.+-\d+', ctx.channel.name):
            await ctx.channel.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(ApplicantCog(bot))
