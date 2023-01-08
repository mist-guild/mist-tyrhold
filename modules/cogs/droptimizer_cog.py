import pandas as pd
import gspread_dataframe as gd
import gspread as gs
import os
from modules.utility.blizzard_utility import BlizzardUtility
from modules.utility.raidsbots_utility import RaidbotsUtility
from modules.utility.gsheets_utility import GoogleSheetsUtility
from discord.ext import commands


class DroptimizerCog(commands.Cog, name="Droptimizer"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.blizz_api = BlizzardUtility()
        self.raidbots = RaidbotsUtility()
        self.sheets_util = GoogleSheetsUtility(os.getenv('SPREADSHEET_NAME'))

    
    @commands.command('droptimizer run')
    async def run_droptimizer_parsing(self):
        # Open the main spreadsheet
        spreadsheet = self.gc.open(self.spreadsheet_name)

        # Get the list of reports from the spreadsheet
        links_sheet = spreadsheet.worksheet('Links')
        mythic_reports_list = [x for x in links_sheet.col_values(2)[1:] if x]
        heroic_reports_list = [x for x in links_sheet.col_values(3)[1:] if x]
        normal_reports_list = [x for x in links_sheet.col_values(4)[1:] if x]

        # Run Reports
        mythic_data = self.raidbots.parse_reports(mythic_reports_list)
        heroic_data = self.raidbots.parse_reports(heroic_reports_list)
        normal_data = self.raidbots.parse_reports(normal_reports_list)

        # Write raw data to the Google Sheet
        self.sheets_util.write_data_to_worksheet('Mythic', mythic_data, include_index=True, include_column_header=True)
        self.sheets_util.write_data_to_worksheet('Heroic', heroic_data, include_index=True, include_column_header=True)
        self.sheets_util.write_data_to_worksheet('Normal', normal_data, include_index=True, include_column_header=True)

        # Get boss summaries
        mythic_summary = self.raidbots.get_boss_summary(mythic_data)
        heroic_summary = self.raidbots.get_boss_summary(heroic_data)
        normal_summary = self.raidbots.get_boss_summary(normal_data)
        self.sheets_util.write_data_to_worksheet('Summary', mythic_data, row=3, col=2)
        self.sheets_util.write_data_to_worksheet('Summary', mythic_data, row=3, col=5)
        self.sheets_util.write_data_to_worksheet('Summary', mythic_data, row=3, col=8)


async def setup(bot: commands.Bot):
    await bot.add_cog(DroptimizerCog(bot))
