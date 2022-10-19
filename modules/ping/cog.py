from discord.ext import commands


class Ping(commands.Cog, name="Ping"):
    """Pings the bot!"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("ping")
    async def ping(self, ctx: commands.Context):
        """Checks for a response from the bot"""
        await ctx.send("Pong")

    @commands.command("cloudz")
    async def cloudz(self, ctx: commands.Context):
        """Tells the truth"""
        for i in range(0, 5):
            await ctx.send("cloudz is a retard!!!")

    @commands.command("enzyte")
    async def enzyte(self, ctx: commands.Context):
        """Tells the truth"""
        for i in range(0, 5):
            await ctx.send("With Enzyte Everybody Wins!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
