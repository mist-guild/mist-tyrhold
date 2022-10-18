import os
from discord.ext import commands

def main():
    client = commands.Bot(command_prefix="?")

    @client.event
    async def on_ready():
        print(f"{client.user.name} has connected to Discord.")

    # load all cogs
    for folder in os.listdir("modules"):
        if os.path.exists(os.path.join("modules", folder, "cog.py")):
            client.load_extension(f"modules.{folder}.cog")

    with open("token.txt", "r") as f:
        token = f.read()
        client.run(token)
        
if __name__ == '__main__':
    main()