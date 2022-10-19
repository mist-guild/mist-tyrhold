import re
from discord.ext import commands
from .trial_utility import TrialUtility


class TrialCog(commands.Cog, name="Trial"):
    """Mist Bot's interaction with trials and the trialing process"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.util = TrialUtility

    @commands.command("trial")
    async def trial(self, ctx: commands.Context, name: str = None, id: int = None):
        """Creates a trial channel - args: <name> <id>"""
        if not ctx.channel.id == 1026048915688140800:
            return

        # check if command args is valid
        if name is None or id is None:
            await ctx.send(
                "Incorrect syntax! Please follow this skeleton: !mb trial <name> <id>")
            return

        # get category and create txt channel
        channel_name = self.util.get_trial_channel_name(name, id)
        channel = await self.util.create_new_trial_channel(ctx.guild, channel_name)
        message = await channel.send(embed=self.util.get_new_trial_embed(name, id))
        await message.pin()

    @commands.command("endtrial")
    async def trial_pass(self, ctx: commands.Context, outcome: str = None):
        """Deletes a trial text channel - args: (optional) <outcome: pass/fail>"""
        if not re.match('.+-\d+', ctx.channel.name):
            return

        if outcome.lower() == "pass":
            await ctx.send("Congrats to the trial!")
            # send msg?
        elif outcome.lower() == "fail":
            await ctx.send("Sadge.")
        await ctx.channel.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(TrialCog(bot))
