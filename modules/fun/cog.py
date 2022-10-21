from discord.ext import commands


class FunCog(commands.Cog, name="Fun"):
    """Fun commands for us to mess with our budzz"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("cloudz", hidden=True)
    async def cloudz(self, ctx: commands.Context):
        for i in range(0, 5):
            await ctx.send("cloudz is a retard!!!")

    @commands.command("enzyte", hidden=True)
    async def enzyte(self, ctx: commands.Context):
        for i in range(0, 5):
            await ctx.send("With Enzyte Everybody Wins!")


async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))
