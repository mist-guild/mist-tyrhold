from discord.ext import commands
from modules.services.reagent_service import ReagentService


class ReagentCog(commands.Cog, name="Reagent"):
    """Tyrhold's interaction with Mist's reagent tracking system"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("reagent")
    async def display_reagent_contribution(self, ctx: commands.Context, character_name):
        """Displays an embed with a guild member's reagent count"""
        embed, reagent = ReagentService.get_reagent_and_embed(character_name)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ReagentCog(bot))
