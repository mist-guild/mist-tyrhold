import datetime
import time


class GeneralUtility:
    @staticmethod
    def get_time_and_date():
        todayVar = datetime.date.today()
        timeVar = time.strftime("%I:%M %p")
        dateVar = todayVar.strftime("%m/%d/%y")
        return timeVar, dateVar
