from discord.ext import commands


class Ping(commands.Cog, name="Ping"):
    """Pings the bot!"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("ping")
    async def ping(self, ctx: commands.Context):
        """Checks for a response from the bot"""
        await ctx.send("Pong")


async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
