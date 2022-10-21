import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!mb ", intents=intents)


async def load_extensions():
    for file in os.listdir("modules"):
        if os.path.exists(os.path.join("modules", file, "cog.py")):
            # cut off the .py from the file name
            await client.load_extension(f"modules.{file}.cog")


async def main():
    async with client:
        await load_extensions()
        await client.start(os.getenv("TOKEN"))

asyncio.run(main())
