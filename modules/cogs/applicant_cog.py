import os
import re
from discord.ext import commands
from modules.services.applicant_service import ApplicantService
from modules.dataclasses.applicant import Applicant
from modules.utility.discord_utility import DiscordUtility


class ApplicantCog(commands.Cog, name="Applicant"):
    """Mist Bot's interaction with applicants and the trialing process"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.category_id != int(os.getenv("RECRUIT_CATEGORY_ID")):
            return

        # post applicant embed
        id = DiscordUtility.get_applicant_id_from_recruit_channel_name(
            channel.name)
        embed, applicant = ApplicantService.get_applicant_and_embed(id)
        message = await channel.send(embed=embed)

        # pin and add reactions
        await message.pin()
        emojis = ["👍", "👎", "💬"]
        for emoji in emojis:
            await message.add_reaction(emoji)

        # check if applicant is already in database
        previous_apps = ApplicantService.get_previous_applications(applicant)
        for id in previous_apps:
            await channel.send(f"**Previous Application detected!** Run `!mb app {id}` to view it.")

    @commands.command("end")
    async def end(self, ctx: commands.Context):
        """Deletes and logs an applicant text channel"""
        if re.match('.{2}-.+-\d+', ctx.channel.name):
            id = DiscordUtility.get_applicant_id_from_recruit_channel_name(
                ctx.channel.name)
            await ApplicantService.archive_comments(id, ctx.channel)
            await ctx.channel.delete()

    @commands.command("app")
    async def app(self, ctx: commands.Context, id):
        """Looks up an applicant by ID"""
        if ctx.channel.category_id != int(os.getenv("RECRUIT_CATEGORY_ID")):
            return

        # create archive channel
        new_channel = await ApplicantService.generate_archive_text_channel(id, ctx.guild)

        # get applicant and post old app
        embed, applicant = ApplicantService.get_applicant_and_embed(id)
        await new_channel.send(embed=embed)

        # post archived messages
        ApplicantService.post_archived_messages(applicant, new_channel)


async def setup(bot: commands.Bot):
    await bot.add_cog(ApplicantCog(bot))
