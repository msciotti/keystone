import requests
from datetime import datetime, timedelta
from disco.types.message import MessageEmbed
from constants import AFFIX_URL,  DUNGEON_LIST, GITHUB_URL, KEYSTONE_ICON_URL


def keystone_insort_right(a, x, lo=0, hi=None):
    if hi is None:
        hi = len(a)

    while lo < hi:
        mid = (lo+hi)//2
        if a[mid].level > x.level:
            lo = mid + 1
        else:
            hi = mid
    a.insert(lo, x)


class Keystone():
    owner = ''
    dungeon = ''
    level = 0

    def __init__(self, name, dungeon, level):
        self.owner = name
        self.dungeon = dungeon
        self.level = level


class KeystoneStorage():
    def __init__(self):
        self.guilds = {}
        self.affixes = {}
        self.timestamp = datetime.utcnow()

    def find_key_by_name(self, guild_id, name):
        for index, keystone in enumerate(self.guilds[guild_id]):
            if keystone.owner == name:
                return index

    def cache(self):
        r = requests.get(AFFIX_URL, timeout=2)
        self.affixes = r.json()
        self.guilds = {}
        now = datetime.utcnow()
        next_tuesday = now + timedelta(days=(1-now.weekday()) % 7)
        if now.weekday() is 1:
            next_tuesday += timedelta(days=7)

        next_tuesday = next_tuesday.replace(hour=16, minute=0)
        self.timestamp = next_tuesday

    def check_cache(self):
        if datetime.utcnow() > self.timestamp:
            self.cache()

    def generate_embed(self, guild_id):
        embed = MessageEmbed()
        names = dungeons = levels = ''

        if self.guilds[guild_id]:
            for keystone in self.guilds[guild_id]:
                names += '\n{}'.format(keystone.owner)
                dungeons += '\n{}'.format(keystone.dungeon)
                levels += '\n{}'.format(keystone.level)
            embed.add_field(name='Character', value=names, inline=True)
            embed.add_field(name='Dungeon', value=dungeons, inline=True)
            embed.add_field(name='Level', value=levels, inline=True)

        for affix in self.affixes['affix_details']:
            embed.add_field(name=affix['name'], value=affix['description'])

        embed.set_author(name='Mythic Keystones',
                         url=GITHUB_URL,
                         icon_url=KEYSTONE_ICON_URL)
        return {'embed': embed}

    def add_key(self, guild_id, name, dungeon, level):
        if dungeon not in DUNGEON_LIST:
            return {'content': '\"{}\" is not a valid dungeon. '
                    'Please use `@keystone dungeons` for a list'
                    ' of valid dungeons.'.format(dungeon)}

        self.check_cache()
        if guild_id not in self.guilds:
            self.guilds[guild_id] = []

        keystone = Keystone(name, DUNGEON_LIST[dungeon], level)

        if self.find_key_by_name(guild_id, name) is not None:
            index = self.find_key_by_name(guild_id, name)
            self.guilds[guild_id][index] = keystone
        else:
            keystone_insort_right(self.guilds[guild_id], keystone)

        return self.generate_embed(guild_id)

    def remove_key(self, guild_id, name):
        if guild_id not in self.guilds:
            return {'content': 'No key found for \"{}\"'.format(name)}

        if not any(keystone.owner == name for keystone in self.guilds[guild_id]):
            return {'content': 'No key found for \"{}\"'.format(name)}

        self.check_cache()

        index = self.find_key_by_name(guild_id, name)
        del self.guilds[guild_id][index]
        return self.generate_embed(guild_id)

