import datetime
import time


class GeneralUtility:
    @staticmethod
    def get_time_and_date():
        todayVar = datetime.date.today()
        timeVar = time.strftime("%I:%M %p")
        dateVar = todayVar.strftime("%m/%d/%y")
        return timeVar, dateVar

    @staticmethod
    def get_class_color_and_icon(class_name):
        class_colors = {
            "Warrior": 0xC79C6E,
            "Paladin": 0xF58CBA,
            "Hunter": 0xABD473,
            "Rogue": 0xFFF569,
            "Priest": 0xFFFFFF,
            "Death Knight": 0xC41F3B,
            "Shaman": 0x0070DE,
            "Mage": 0x69CCF0,
            "Warlock": 0x9482C9,
            "Monk": 0x00FF96,
            "Druid": 0xFF7D0A,
            "Demon Hunter": 0xA330C9,
            "Evoker": 0x33937F,
        }

        class_icons = {
            "Warrior": '<:Warrior:976616539744792616>',
            "Paladin": '<:Paladin:976616493859078155>',
            "Hunter": '<:Hunter:976616446752874536>',
            "Rogue": '<:Rogue:976616482190528582>',
            "Priest": '<:Priest:976616470391955467>',
            "Death Knight": '<:DeathKnight:976616412288282634>',
            "Shaman": '<:Shaman:976616510183313408> ',
            "Mage": '<:Mage:976616436585881700>',
            "Warlock": '<:Warlock:976616527526768680>',
            "Monk": '<:Monk:976616424699215922> ',
            "Druid": '<:Druid:976616457406390332>',
            "Demon Hunter": '<:DemonHunter:976616398912618517>',
            "Evoker": '<:evoker_flat:1034823772290695259>',
        }

        return class_colors[class_name], class_icons[class_name]
