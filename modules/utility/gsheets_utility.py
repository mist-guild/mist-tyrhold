import gspread
import gspread_dataframe as gs_df
import pandas


class GoogleSheetsUtility:

    def __init__(self, spreadsheet_name: str):
        self.gc = gspread.service_account(filename='creds.json')
        self.spreadsheet = self.gc.open(spreadsheet_name)


    def get_worksheet(self, name):
        return self.spreadsheet.worksheet(name)

    
    def write_data_to_worksheet(self, worksheet_name, data, row=0, col=0, include_index=False, include_column_header=False, resize=True):
        dataframe = pandas.DataFrame(data=data)
        gs_df.set_with_dataframe(worksheet=self.get_worksheet(worksheet_name), dataframe=dataframe, row=row, col=col,
            include_index=include_index, include_column_header=include_column_header, resize=resize)

