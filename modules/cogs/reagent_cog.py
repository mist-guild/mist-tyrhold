from discord.ext import commands


class ReagentCog(commands.Cog, name="Reagent"):
    """Fun commands for us to mess with our budzz"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("reagent")
    async def end(self, ctx: commands.Context, reagent):
        """Deletes and logs an applicant text channel"""
        if re.match('.{2}-.+-\d+', ctx.channel.name):
            id = DiscordUtility.get_applicant_id_from_recruit_channel_name(
                ctx.channel.name)
            await ApplicantService.archive_comments(id, ctx.channel)
            await ctx.channel.delete()
    


async def setup(bot: commands.Bot):
    await bot.add_cog(ReagentCog(bot))
