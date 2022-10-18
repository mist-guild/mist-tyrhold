import os
import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="?", intents=intents)


async def load_extensions():
    for file in os.listdir("modules"):
        if os.path.exists(os.path.join("modules", file, "cog.py")):
            # cut off the .py from the file name
            await client.load_extension(f"modules.{file}.cog")


async def main():
    token = open("token.txt", "r").read()
    async with client:
        await load_extensions()
        await client.start(token)

asyncio.run(main())
