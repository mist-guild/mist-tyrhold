import asyncio
import random
import discord
from discord.ext import commands

class WindbridgeCog(commands.Cog, name="Windbridge"):
    """Mist Bot's windbridge specific commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Loot Council
        self.lc_ineligible = []
    
    @commands.command("lootcouncil")
    async def randomize_loot_council(self, ctx: commands.Context):
        '''Randomizes a person from the roster to use for the loot council.'''
        # Get the Windbridge roster from a list of Discord members with Windbridge Role
        roster = []
        for role in ctx.guild.roles:
            if role.name == 'Windbridge Raider':
                roster = role.members
        for user in roster:
            for role in user.roles:
                if role.name == 'Windbridge Officer':
                    roster.remove(user)

        # Get the Random Person this week
        raider = random.choice(roster)

        # Move them to the ineligible list
        roster.remove(raider)
        self.lc_ineligible.append(raider)

        # Build the message
        message += 'Eligible Raiders:\n'
        for e in roster:
            message += e.nick + '\n'
        message += '\n\nIneligble Raiders:\n'
        for i in self.lc_ineligible:
            message += i.nick + '\n'

        message += "This week's choice: " + raider.nick

        # Send the message
        ctx.channel.send("```" + message + "```")


    @commands.command("lc_reset")
    async def reset_loot_council(self, ctx: commands.Context):
        '''Resets the roster for loot council, clearing the ineligible list.'''
        self.lc_ineligible = []

async def setup(bot: commands.Bot):
    await bot.add_cog(WindbridgeCog(bot))