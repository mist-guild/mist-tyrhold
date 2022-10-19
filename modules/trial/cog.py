import discord
from discord.ext import commands
from .trial_utility import TrialUtility


class TrialCog(commands.Cog, name="Trial"):
    """Mist Bot's interaction with trials and the trialing process"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("trial")
    async def trial(self, ctx: commands.Context, name: str, id: int):
        """Creates a trial channel - args: <name> <id>"""
        # check if command args is valid
        if name is None or id is None:
            ctx.send(
                "Incorrect syntax! Please follow this skeleton: !mb trial <name> <id>")
            return
        
        # get category and create txt channel
        channel_name = TrialUtility.get_trial_channel_name(name, id)
        TrialUtility.create_new_trial_channel(ctx.guild, channel_name)


async def setup(bot: commands.Bot):
    await bot.add_cog(TrialCog(bot))
