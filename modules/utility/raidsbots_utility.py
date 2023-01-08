import requests
import csv

class RaidbotsUtility:

    def get_report_csv(self, report_link):
        '''
        Downloads the Report Data from Raidbots using the Simple CSV data endpoint.
        '''
        report_link = report_link + '/data.csv'
        raw_data = None
        with requests.Session() as s:
            raw_data = s.get(report_link)
        decoded_content = raw_data.content.decode('utf-8')
        csv_data = csv.reader(decoded_content.splitlines(), delimiter=',')
        data_list = list(csv_data)
        return data_list


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


    def parse_reports(self, report_list):
        mythic_data = {}
        if len(report_list) > 0:
            for report_link in report_list:
                # Download report data
                report_data = self.get_report_csv(report_link)
                player, data = self.parse_report(report_data)
                mythic_data[player] = data
        return mythic_data

    
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