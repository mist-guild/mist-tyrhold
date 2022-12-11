from apis.valdrakken import Valdrakken
from apis.dataclasses.reagent import Reagent
from modules.utility.general_utility import GeneralUtility
import discord


class ReagentService:
    @staticmethod
    def get_reagent_and_embed(character_name):
        reagent = Reagent.build_reagent_from_character_name(character_name)
        if reagent is None:
            embed = discord.Embed(
                description=f"No reagent data found for {character_name}.", color=0xFFD71C)
            return embed, None

        # build embed
        time, date = GeneralUtility.get_time_and_date()
        embed = discord.Embed(title=f":hammer_pick: Reagent Summmary for {reagent.character_name}",
                              description=f"This summary was posted at {time} on {date}.", color=0xFFD71C)

        # line break
        embed.add_field(name="\u200B", value="\u200B", inline=False)

        # thing
        embed.add_field(name=":herb: Hochenblume",
                        value=f"""
                        <:tier1:1046594007695884368> {reagent.hochenblume_bronze}\n
                        <:tier2:1046594008568311949> 0\n
                        <:tier3:1046594009390403594> 0\n
                        """,
                        inline=True)

        embed.add_field(name="\u200B", value="\u200B", inline=True)

        embed.add_field(name="🐮 Bubble Poppy",
                        value=f"""
                        <:tier1:1046594007695884368> {reagent.bubble_poppy_bronze}\n
                        <:tier2:1046594008568311949> {reagent.bubble_poppy_silver}\n
                        <:tier3:1046594009390403594> 0\n
                        """,
                        inline=True)

        # line space
        embed.add_field(name="\u200B", value="\u200B", inline=False)

        embed.add_field(name=":rock: Writhebark",
                        value=f"""
                        <:tier1:1046594007695884368> 0\n
                        <:tier2:1046594008568311949> 0\n
                        <:tier3:1046594009390403594> {reagent.writhebark_gold}\n
                        """,
                        inline=True)

        embed.add_field(name="\u200B", value="\u200B", inline=True)

        embed.add_field(name="🐮 Bubble Poppy",
                        value=f"""
                        <:tier1:1046594007695884368> {reagent.bubble_poppy_bronze}\n
                        <:tier2:1046594008568311949> {reagent.bubble_poppy_silver}\n
                        <:tier3:1046594009390403594> 0\n
                        """,
                        inline=True)
        return embed, reagent
