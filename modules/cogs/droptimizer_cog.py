import pandas as pd
import gspread_dataframe as gd
import gspread as gs
import os
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

    
    @commands.command('droptimizer')
    async def run_droptimizer_parsing(self, ctx: commands.Context):
        await ctx.channel.send('Beginning parsing.')

        # Get the list of reports from the spreadsheet
        links_sheet = self.sheets_util.get_worksheet('Links')
        mythic_reports_list = [x for x in links_sheet.col_values(2)[1:] if x]
        heroic_reports_list = [x for x in links_sheet.col_values(3)[1:] if x]
        normal_reports_list = [x for x in links_sheet.col_values(4)[1:] if x]
        await ctx.channel.send('Retrieved report links.')

        # Run Reports
        mythic_data = self.droptimizer_service.parse_reports(mythic_reports_list)
        heroic_data = self.droptimizer_service.parse_reports(heroic_reports_list)
        normal_data = self.droptimizer_service.parse_reports(normal_reports_list)
        await ctx.channel.send('Parsed raw data.')

        # Write raw data to the Google Sheet
        self.sheets_util.write_data_to_worksheet('Mythic', mythic_data, include_index=True, include_column_header=True)
        self.sheets_util.write_data_to_worksheet('Heroic', heroic_data, include_index=True, include_column_header=True)
        self.sheets_util.write_data_to_worksheet('Normal', normal_data, include_index=True, include_column_header=True)
        await ctx.channel.send('Wrote raw data to spreadsheet.')

        # Get boss summaries
        mythic_summary = self.droptimizer_service.get_boss_summary(mythic_data)
        heroic_summary = self.droptimizer_service.get_boss_summary(heroic_data)
        normal_summary = self.droptimizer_service.get_boss_summary(normal_data)
        await ctx.channel.send('Generated boss summaries.')

        # Write Summary Data
        self.sheets_util.write_data_to_worksheet('Summary', mythic_summary, row=3, col=2)
        self.sheets_util.write_data_to_worksheet('Summary', heroic_summary, row=3, col=5)
        self.sheets_util.write_data_to_worksheet('Summary', normal_summary, row=3, col=8)
        await ctx.channel.send('Wrote boss summaries to spreadsheet.')


async def setup(bot: commands.Bot):
    await bot.add_cog(DroptimizerCog(bot))
