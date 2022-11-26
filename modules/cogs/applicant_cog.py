import os
import re
import asyncio
from discord.ext import commands
import requests
from modules.services import applicant_service


class ApplicantCog(commands.Cog, name="Applicant"):
    """Mist Bot's interaction with applicants and the trialing process"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.category_id != int(os.getenv("RECRUIT_CATEGORY_ID")):
            return

        # post applicant embed
        embed, applicant = applicant_service.build_applicant_embed(
            channel.name)
        message = await channel.send(embed=embed)

        # pin and add reactions
        await message.pin()
        emojis = ["👍", "👎", "💬"]
        for emoji in emojis:
            await message.add_reaction(emoji)

        # check if applicant is already in database
        previous_apps = applicant_service.get_previous_applications(applicant)
        for id in previous_apps:
            await channel.send(f"**Previous Application detected!** Run `!mb app {id}` to view it.")

    @commands.command("end")
    async def end(self, ctx: commands.Context):
        """Deletes and logs an applicant text channel"""
        if re.match('.{2}-.+-\d+', ctx.channel.name):
            await applicant_service.archive_comments(ctx.channel)
            await ctx.channel.delete()

    @commands.command("app")
    async def app(self, ctx: commands.Context, id):
        """Looks up an applicant by ID"""
        if ctx.channel.category_id != int(os.getenv("RECRUIT_CATEGORY_ID")):
            return

        # get applicant
        applicant = applicant_service.build_applicant_from_id(id)

        # create archive channel
        channel_name = applicant_service.get_archive_channel_name(applicant)
        new_channel = await applicant_service.create_text_channel(ctx.guild, channel_name)

        # post application and messaages
        embed = applicant_service.build_applicant_embed(applicant)
        await new_channel.send(embed=embed)
        if applicant.archived_comments:
            messages = applicant.decode_archived_comments()
            messages_split = [messages[i:i+1000]
                              for i in range(0, len(messages), 1000)]
            for message in messages_split:
                await new_channel.send(message, suppress_embeds=True)
                await asyncio.sleep(2)


async def setup(bot: commands.Bot):
    await bot.add_cog(ApplicantCog(bot))
