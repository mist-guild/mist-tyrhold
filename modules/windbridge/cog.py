import os
import re
import asyncio
import random
import discord
from discord.ext import commands
import requests

roster = [
    'Ani', 'AP', 'Atlas',
    'Carande', 'Cbreez', 'Dallas',
    'Ducky', 'Haasbeen', 'Hmac', 'Hoogita',
    'Impatients', 'Jangoz', 'Londin', 'Malicarie',
    'Max', 'Mysticplay', 'Nicaras', 'Noramage',
    'Plutar', 'Rhazkala', 'Trum', 'Ulchi', 'Zensy'
]

class WindbridgeCog(commands.Cog, name="Windbridge"):
    """Mist Bot's windbridge specific commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Loot Council
        self.lc_eligible = [''.join(x) for x in roster]
        self.lc_ineligible = []
    
    @commands.command("lootcouncil")
    async def randomize_loot_council(self, ctx: commands.Context):
        '''Randomizes a person from the roster to use for the loot council.'''
        # Get the Random Person this week
        raider = random.choice(self.lc_eligible)

        # Move them to the ineligible list
        self.lc_eligible.remove(raider)
        self.lc_ineligible.append(raider)

        # Build the message
        message += 'Eligible Raiders:\n'
        for e in self.lc_eligible:
            message += e + '\n'
        
        message += '\n\nIneligble Raiders:\n'
        for i in self.lc_ineligible:
            message += i + '\n'

        message += "This week's choice: " + raider

        # Send the message
        ctx.channel.send("```" + message + "```")


    @commands.command("lc_reset")
    async def reset_loot_council(self, ctx: commands.Context):
        '''Resets the roster for loot council, clearing the ineligible list.'''
        self.lc_eligible = [''.join(x) for x in roster]
        self.lc_ineligible = []
