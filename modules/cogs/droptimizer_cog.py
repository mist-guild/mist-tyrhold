import gspread_dataframe as gd
import os
import pandas
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
        '''Parses all input Droptimizer Links.'''
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

        # Add 'Boss' to Cell A1
        self.sheets_util.get_worksheet('Mythic').update('A1', 'Boss')
        self.sheets_util.get_worksheet('Heroic').update('A1', 'Boss')
        self.sheets_util.get_worksheet('Normal').update('A1', 'Boss')

        # Get boss summaries
        mythic_summary = self.droptimizer_service.get_boss_summary(mythic_data)
        heroic_summary = self.droptimizer_service.get_boss_summary(heroic_data)
        normal_summary = self.droptimizer_service.get_boss_summary(normal_data)

        # Write Summary Data
        self.sheets_util.write_data_to_worksheet('Summary', pandas.DataFrame(data=mythic_summary).transpose().sort_index(), row=3, col=1, include_index=True, resize=False)
        self.sheets_util.write_data_to_worksheet('Summary', pandas.DataFrame(data=heroic_summary).transpose().sort_index(), row=3, col=5, resize=False)
        self.sheets_util.write_data_to_worksheet('Summary', pandas.DataFrame(data=normal_summary).transpose().sort_index(), row=3, col=8, resize=False)
        await ctx.channel.send('```Droptimizer run completed.```')


    @commands.command('droptimizer_search')
    async def get_droptimizer_boss_list(self, ctx: commands.Context, difficulty: str, search_name: str):
        '''
        Gets a list of Players and their highest upgrades for the input boss.
        '''
        # Check parameters for validity
        if difficulty not in ['Mythic', 'Heroic', 'Normal']:
            await ctx.channel.send('Invalid difficulty. Valid options: Mythic, Heroic, Normal')
            return

        try:
            # Get full data for the difficulty
            worksheet = self.sheets_util.get_worksheet(difficulty)
            dataframe = gd.get_as_dataframe(worksheet=worksheet).set_index('Boss')
            dataframe = dataframe.filter(like=search_name, axis=0).fillna(0)
            max_values = dataframe.max(axis=0).sort_values(ascending=False)
            max_val = pandas.DataFrame(max_values)
            max_item = pandas.DataFrame(dataframe.idxmax())
            concat = pandas.concat([max_val, max_item], axis=1)
            
            response_list = []
            for index, row in concat.iterrows():
                row_list = [x for x in row.values]
                name = index
                value = '{:>,.0f}'.format(row_list[0])
                item = row_list[1].split(' - ')[1]
                response_list.append('{0:15} | {1:>5} | {2}\n'.format(name, value, item))

            response = ''
            for resp in response_list:
                response += resp
                if len(response) > 1800:
                    await ctx.channel.send('```' + response + '```')
                    response = ''
            await ctx.channel.send('```' + response + '```')
            
        except Exception as e:
            print(e)
        


async def setup(bot: commands.Bot):
    await bot.add_cog(DroptimizerCog(bot))
