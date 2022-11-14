import os
import re
from discord.ext import commands
import requests
from . import utility


class ApplicantCog(commands.Cog, name="Applicant"):
    """Mist Bot's interaction with applicants and the trialing process"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.category_id != int(os.getenv("RECRUIT_CATEGORY_ID")):
            return

        # post applicant embed
        id = utility.get_applicant_id(channel.name)
        applicant = utility.build_applicant_from_id(id)
        embed = utility.build_applicant_embed(applicant)
        message = await channel.send(embed=embed)

        # pin and add reactions
        await message.pin()
        emojis = ["👍", "👎", "💬"]
        for emoji in emojis:
            await message.add_reaction(emoji)

    @commands.command("end")
    async def end(self, ctx: commands.Context):
        """Deletes an applicant text channel"""
        if re.match('.{2}-.+-\d+', ctx.channel.name):
            id = utility.get_applicant_id(ctx.channel.name)
            archived_comments = await utility.get_archive_comments_string(
                ctx.channel)
            requests.put(f"http://127.0.0.1:5000/applicant/archive/{id}",
                         data=archived_comments,
                         headers={'Content-Type': 'application/octet-stream'})

    @commands.command("app")
    async def app(self, ctx: commands.Context, id):
        """Looks up an applicant by ID"""
        # if ctx.channel.category_id != int(os.getenv("RECRUIT_CATEGORY_ID")):
        #     return

        applicant = utility.build_applicant_from_id(id)
        embed = utility.build_applicant_embed(applicant)
        # post all comments
        await ctx.channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ApplicantCog(bot))
