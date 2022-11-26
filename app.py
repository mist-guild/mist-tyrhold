import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from discord import Embed, Emoji

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!mb ", intents=intents)


async def load_extensions():
    # os.listdir("modules") - dev
    # os.listdir("/home/mistguild/bot/modules") - prod
    for file in os.listdir("modules/cogs"):
        if file.startswith("__pycache__"):
            continue
        await client.load_extension(f"modules.cogs.{file[:-3]}")


async def main():
    async with client:
        await load_extensions()
        await client.start(os.getenv("TOKEN"))

asyncio.run(main())
