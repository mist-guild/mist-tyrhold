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