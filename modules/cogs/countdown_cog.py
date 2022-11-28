from discord.ext import commands
import discord


class CountdownCog(commands.Cog, name="Countdown"):
    """Tyrhold's countdown timer functionality"""
    # TODO: add a service to handle the countdowns

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("countdown-create")
    async def countdown(self, ctx, *, args):
        """Creates a countdown embed."""
        args = args.split("---")
        dic = {}
        for arg in args:
            arg_split = arg.split("::")
            dic[arg_split[0].strip()] = arg_split[1].strip()

        embed = discord.Embed(title=f"{ dic['title'] } is <t:{ int(dic['time']) }:R>",
                              description=f"{ dic['title'] } occurs on <t:{ int(dic['time']) }:F>. Click the title to see a more detailed countdown!",
                              url=f"https://www.epochconverter.com/countdown?q={ int(dic['time']) }")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

        if "color" in dic:
            if "#" in dic["color"]:
                dic["color"] = dic["color"][1:]
            embed.color = int(dic['color'], 16)
        if "image" in dic:
            embed.set_image(url=dic['image'])
        if "thumbnail" in dic:
            embed.set_thumbnail(url=dic['thumbnail'])

        await ctx.channel.send(embed=embed)

    @commands.command("countdown-template")
    async def countdown_template(self, ctx):
        """Displays an embed with a countdown template."""
        embed = discord.Embed(title="**🕒 Tyrhold's Countdown Template**",
                              description="""
                              !mb countdown create title:: [title] --- time:: [time] --- color:: [color] --- image:: [image] --- thumbnail:: [thumbnail]
                              \nConvert your desired time to Unix time [here](https://www.epochconverter.com/). The only required fields are title and time; the rest can be removed.
                              """)
        await ctx.channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CountdownCog(bot))
