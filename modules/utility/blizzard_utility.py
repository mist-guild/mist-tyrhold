from blizzardapi import BlizzardApi
import os
import json

# DK, DH, Lock
DREADFUL_HELM = '196590'
DREADFUL_SHOULDERS = '196589'
DREADFUL_CHEST = '196586'
DREADFUL_GLOVES = '196587'
DREADFUL_PANTS = '196588'

# Druid, Hunter, Mage
MYSTIC_HELM = '196600'
MYSTIC_SHOULDERS = '196599'
MYSTIC_CHEST = '196596'
MYSTIC_GLOVES = '196597'
MYSTIC_PANTS = '196598'

# Paladin, Priest, Shaman
VENERATED_HELM = '196605'
VENERATED_SHOULDERS = '196604'
VENERATED_CHEST = '196601'
VENERATED_GLOVES = '196602'
VENERATED_PANTS = '196603'

# Evoker, Monk, Rogue, Warrior
ZENITH_HELM = '196595'
ZENITH_SHOULDERS = '196594'
ZENITH_CHEST = '196591'
ZENITH_GLOVES = '196592'
ZENITH_PANTS = '196593'

TIER_LIST = {

    # Death Knight
    '200405': DREADFUL_CHEST,
    '200407': DREADFUL_GLOVES,
    '200408': DREADFUL_HELM,
    '200409': DREADFUL_PANTS,
    '200410': DREADFUL_SHOULDERS,

    # Demon Hunter
    '200342': DREADFUL_CHEST,
    '200344': DREADFUL_GLOVES,
    '200345': DREADFUL_HELM,
    '200346': DREADFUL_PANTS,
    '200347': DREADFUL_SHOULDERS,

    # Druid
    '200351': MYSTIC_CHEST,
    '200353': MYSTIC_GLOVES,
    '200354': MYSTIC_HELM,
    '200355': MYSTIC_PANTS,
    '200356': MYSTIC_SHOULDERS,

    # Evoker
    '200378': ZENITH_CHEST,
    '200380': ZENITH_GLOVES,
    '200381': ZENITH_HELM,
    '200382': ZENITH_PANTS,
    '200383': ZENITH_SHOULDERS,

    # Hunter
    '200351': MYSTIC_CHEST,
    '200353': MYSTIC_GLOVES,
    '200354': MYSTIC_HELM,
    '200355': MYSTIC_PANTS,
    '200356': MYSTIC_SHOULDERS,

    # Mage
    '200315': MYSTIC_CHEST,
    '200317': MYSTIC_GLOVES,
    '200318': MYSTIC_HELM,
    '200319': MYSTIC_PANTS,
    '200320': MYSTIC_SHOULDERS,

    # Monk
    '200360': ZENITH_CHEST,
    '200362': ZENITH_GLOVES,
    '200363': ZENITH_HELM,
    '200364': ZENITH_PANTS,
    '200365': ZENITH_SHOULDERS,

    # Paladin
    '200414': VENERATED_CHEST,
    '200416': VENERATED_GLOVES,
    '200417': VENERATED_HELM,
    '200418': VENERATED_PANTS,
    '200419': VENERATED_SHOULDERS,

    # Priest
    '200324': VENERATED_CHEST,
    '200326': VENERATED_GLOVES,
    '200327': VENERATED_HELM,
    '200328': VENERATED_PANTS,
    '200329': VENERATED_SHOULDERS,

    # Rogue
    '200360': ZENITH_CHEST,
    '200362': ZENITH_GLOVES,
    '200363': ZENITH_HELM,
    '200364': ZENITH_PANTS,
    '200365': ZENITH_SHOULDERS,

    # Shaman
    '200396': VENERATED_CHEST,
    '200398': VENERATED_GLOVES,
    '200399': VENERATED_HELM,
    '200400': VENERATED_PANTS,
    '200401': VENERATED_SHOULDERS,

    # Warlock
    '200333': DREADFUL_CHEST,
    '200335': DREADFUL_GLOVES,
    '200336': DREADFUL_HELM,
    '200337': DREADFUL_PANTS,
    '200338': DREADFUL_SHOULDERS,

    # Warrior
    '200423': ZENITH_CHEST,
    '200425': ZENITH_GLOVES,
    '200426': ZENITH_HELM,
    '200427': ZENITH_PANTS,
    '200428': ZENITH_SHOULDERS,
}

class BlizzardUtility:

    def __init__(self):
        self.api_client = BlizzardApi(os.getenv('BLIZZ_CLIENT'), os.getenv('BLIZZ_SECRET'))
        self.boss_list = {
            '-44': 'Trash',
        }
        self.item_list = {}
        if os.path.exists('blizz_cache.json'):
            self.load_cache()


    def get_boss(self, id):
        '''
        Retrieves boss information from the Blizzard WoW GameData API using the encounter id.
        '''
        if id not in self.boss_list:
            boss = self.api_client.wow.game_data.get_journal_encounter('us', 'en_US', id)
            self.boss_list[id] = boss['name']
            self.save_cache()
        return self.boss_list[id]


    def get_item(self, id):
        '''
        Retrieves item information from the Blizzard WoW GameData API using the item id.
        '''
        if id in TIER_LIST:
            id = TIER_LIST[id]
        if id not in self.item_list:
            item = self.api_client.wow.game_data.get_item('us', 'en_US', id)
            self.item_list[id] = item['name']
            self.save_cache()
        return self.item_list[id]


    def save_cache(self):
        cache = {
            'boss': self.boss_list,
            'item': self.item_list
        }
        with open('blizz_cache.json','w') as f:
            f.write(json.dumps(cache))


    def load_cache(self):
        cache = None
        with open('blizz_cache.json', 'r') as f:
            cache = json.loads(f.read())
        self.boss_list = cache['boss']
        self.item_list = cache['item']