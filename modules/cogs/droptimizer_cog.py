import pandas as pd
import gspread_dataframe as gd
import gspread as gs
import os
import pandas
import discord
from tabulate import tabulate
from modules.utility.blizzard_utility import BlizzardUtility
from modules.utility.raidbots_utility import RaidbotsUtility
from modules.utility.gsheets_utility import GoogleSheetsUtility
from modules.services.droptimizer_service import DroptimizerService
from discord.ext import commands


class DroptimizerCog(commands.Cog, name="Droptimizer"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.droptimizer_service = DroptimizerService()
        self.sheets_util = GoogleSheetsUtility(os.getenv('SPREADSHEET_NAME'))

    
    @commands.command(name="droptimizer_run")
    async def run_droptimizer_reports(self, ctx: commands.Context):

        # Get the list of reports from the spreadsheet
        links_sheet = self.sheets_util.get_worksheet('Links')
        mythic_reports_list = [x for x in links_sheet.col_values(2)[1:] if x]
        heroic_reports_list = [x for x in links_sheet.col_values(3)[1:] if x]
        normal_reports_list = [x for x in links_sheet.col_values(4)[1:] if x]

        # Run Reports
        mythic_data = self.droptimizer_service.parse_reports(mythic_reports_list)
        heroic_data = self.droptimizer_service.parse_reports(heroic_reports_list)
        normal_data = self.droptimizer_service.parse_reports(normal_reports_list)

        # Write raw data to the Google Sheet
        self.sheets_util.write_data_to_worksheet('Mythic', pandas.DataFrame(data=mythic_data), include_index=True, include_column_header=True)
        self.sheets_util.write_data_to_worksheet('Heroic', pandas.DataFrame(data=heroic_data), include_index=True, include_column_header=True)
        self.sheets_util.write_data_to_worksheet('Normal', pandas.DataFrame(data=normal_data), include_index=True, include_column_header=True)

        # Get boss summaries
        mythic_summary = self.droptimizer_service.get_boss_summary(mythic_data)
        heroic_summary = self.droptimizer_service.get_boss_summary(heroic_data)
        normal_summary = self.droptimizer_service.get_boss_summary(normal_data)

        # Write Summary Data
        self.sheets_util.write_data_to_worksheet('Summary', pandas.DataFrame(data=mythic_summary).transpose().sort_index(), row=3, col=1, include_index=True, resize=False)
        self.sheets_util.write_data_to_worksheet('Summary', pandas.DataFrame(data=heroic_summary).transpose().sort_index(), row=3, col=5, resize=False)
        self.sheets_util.write_data_to_worksheet('Summary', pandas.DataFrame(data=normal_summary).transpose().sort_index(), row=3, col=8, resize=False)
        await ctx.channel.send('```Droptimizer run completed.```')


    @commands.command('droptimizer_boss')
    async def get_droptimizer_boss_list(self, ctx: commands.Context, difficulty: str, boss_name: str):
        # Check parameters for validity
        if difficulty not in ['Mythic', 'Heroic', 'Normal']:
            await ctx.channel.send('Invalid difficulty. Valid options: Mythic, Heroic, Normal')
            return
        if boss_name not in ['Eranog', 'Terros', 'Sennarth', 'Kurog', 'Council', 'Dathea', 'Broodkeeper', 'Raszageth']:
            await ctx.channel.send('Invalid Boss. Valid options: Eranog, Terros, Sennarth, Kurog, Council, Dathea, Broodkeeper, Raszageth')
            return

        try:
            # Get full data for the difficulty
            worksheet = self.sheets_util.get_worksheet(difficulty)
            dataframe = gd.get_as_dataframe(worksheet=worksheet).set_index('Boss')
            dataframe = dataframe.filter(like=boss_name, axis=0)
            max_values = dataframe.max(axis=0).sort_values(ascending=False)
            df = pandas.DataFrame(max_values)

            # Create an Embed with the info
            await ctx.send('```'+ difficulty + ' ' + boss_name + '\n' + tabulate(df, headers='keys', tablefmt='psql')+'```')
        except Exception as e:
            print(e)
        


async def setup(bot: commands.Bot):
    await bot.add_cog(DroptimizerCog(bot))
