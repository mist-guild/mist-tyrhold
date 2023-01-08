import pandas as pd
import gspread_dataframe as gd
import gspread as gs
import os
from modules.utility.blizzard_utility import BlizzardUtility
from modules.utility.raidsbots_utility import RaidbotsUtility
from discord.ext import commands


class DroptimizerCog(commands.Cog, name="Droptimizer"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.gc = gs.service_account(filename='creds.json')
        self.spreadsheet_name = os.getenv('SPREADSHEET_NAME')
        self.blizz_api = BlizzardUtility()

    
    @commands.command('droptimizer run')
    async def run_droptimizer_parsing(self):
        # Open the main spreadsheet
        spreadsheet = self.gc.open(self.spreadsheet_name)

        # Get the list of reports from the spreadsheet
        links_sheet = spreadsheet.worksheet('Links')
        mythic_reports_list = [x for x in links_sheet.col_values(2)[1:] if x]
        heroic_reports_list = [x for x in links_sheet.col_values(3)[1:] if x]
        normal_reports_list = [x for x in links_sheet.col_values(4)[1:] if x]

        # Run Mythic Parses
        mythic_dataframe = None
        mythic_data = {}
        if len(mythic_reports_list) > 0:
            for report_link in mythic_reports_list:
                # Download report data
                report_data = RaidbotsUtility.get_report_csv(report_link)
                player, data = self.parse_report(report_data)
                mythic_data[player] = data
            mythic_dataframe = pd.DataFrame(data=mythic_data)
            mythic_sheet = spreadsheet.worksheet('Mythic')
            self.write_dataframe_to_sheet(mythic_dataframe, mythic_sheet)

        # Run Heroic Parses
        heroic_dataframe = None
        heroic_data = {}
        if len(heroic_reports_list) > 0:
            for report_link in heroic_reports_list:
                # Download report data
                report_data = RaidbotsUtility.get_report_csv(report_link)
                player, data = self.parse_report(report_data)
                heroic_data[player] = data
            heroic_dataframe = pd.DataFrame(data=heroic_data)
            heroic_sheet = spreadsheet.worksheet('Heroic')
            self.write_dataframe_to_sheet(heroic_dataframe, heroic_sheet)

        # Run Normal Parses
        normal_dataframe = None
        normal_data = {}
        if len(normal_reports_list) > 0:
            for report_link in normal_reports_list:
                # Download report data
                report_data = RaidbotsUtility.get_report_csv(report_link)
                player, data = self.parse_report(report_data)
                normal_data[player] = data
            normal_dataframe = pd.DataFrame(data=normal_data)
            normal_sheet = spreadsheet.worksheet('Normal')
            self.write_dataframe_to_sheet(normal_dataframe, normal_sheet)

        # Get boss summaries
        summary_sheet = spreadsheet.worksheet('Summary')
        if mythic_dataframe is not None:
            mythic_summary = self.get_boss_summary(mythic_data)
            summary_dataframe = pd.DataFrame(data=mythic_summary).transpose().sort_index()
            gd.set_with_dataframe(worksheet=summary_sheet, dataframe=summary_dataframe,
                row=3, col=2, include_index=False, include_column_header=False)
        if heroic_dataframe is not None:
            heroic_summary = self.get_boss_summary(heroic_data)
            summary_dataframe = pd.DataFrame(data=heroic_summary).transpose().sort_index()
            gd.set_with_dataframe(worksheet=summary_sheet, dataframe=summary_dataframe,
                row=3, col=5, include_index=False, include_column_header=False)
        if normal_dataframe is not None:
            normal_summary = self.get_boss_summary(normal_data)
            summary_dataframe = pd.DataFrame(data=normal_summary).transpose().sort_index()
            gd.set_with_dataframe(worksheet=summary_sheet, dataframe=summary_dataframe,
                row=3, col=8, include_index=False, include_column_header=False)


    def write_dataframe_to_sheet(self, data, sheet):
        '''
        Writes a dataframe to the specified sheet
        '''
        sheet.clear()
        gd.set_with_dataframe(worksheet=sheet,dataframe=data,include_index=True,include_column_header=True,resize=True)


    def get_boss_summary(self, data: dict):
        '''
        Grabs relevant statistics for each boss
        '''
        boss_data = {

        }
        for player in data:
            player_data = {}
            
            # Get the highest upgrade for each Encounter
            for item in data[player]:
                item_list = item.split('-')
                boss_name = item_list[0].strip()
                item_name = item_list[1].strip()
                if boss_name not in player_data:
                    player_data[boss_name] = 0
                upgrade_value = max(0, data[player][item])
                player_data[boss_name] += upgrade_value
            
            # Add player data to for boss
            for boss in player_data:
                # If the boss is not in the data, add it and initialize its value
                if boss not in boss_data:
                    boss_data[boss] = {
                        'count': 0,
                        'total': 0,
                        'max': 0
                    }
                upgrade_value = player_data[boss]
                if upgrade_value > 100:
                    boss_data[boss]['count'] += 1
                    boss_data[boss]['total'] += upgrade_value
                    boss_data[boss]['max'] = max(boss_data[boss]['max'], upgrade_value)

        return boss_data


    def parse_report(self, data):
        '''
        Parses the data in a raidbots data.csv to find the % increase for each sim reported
        '''
        player = data[1][0]
        print('Parsing report for player ' + player + '.')

        report_data = {}

        # Get the Report Data
        baseline_dps = float(data[1][1])
        for sim in data[2:]:
            # Calculate the Sim Info
            sim_dps = float(sim[1])
            sim_diff = (sim_dps - baseline_dps)

            # Get the Item Name
            sim_name_list = sim[0].split('/')
            item_name = self.blizz_api.get_boss(sim_name_list[1]) + ' - ' + self.blizz_api.get_item(sim_name_list[3])

            # Add to data dictionary, choosing the highest sim if the item appears multiple times
            if item_name in report_data:
                report_data[item_name] = max(sim_diff, report_data[item_name])
            else:
                report_data[item_name] = sim_diff

        return player, report_data


async def setup(bot: commands.Bot):
    await bot.add_cog(DroptimizerCog(bot))
