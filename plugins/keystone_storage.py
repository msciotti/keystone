import requests
import json
from collections import defaultdict
from datetime import datetime, timedelta
from disco.types.message import MessageEmbed
from constants import AFFIX_URL,  DUNGEON_LIST, GITHUB_URL, KEYSTONE_ICON_URL


class KeystoneStorage():
    keys = defaultdict(dict)
    affixes = {}
    timestamp = datetime.utcnow()

    def cache(self):
        r = requests.get(AFFIX_URL, timeout=2)
        self.affixes = r.json()
        self.keys = defaultdict(dict)
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
        keys = ''

        for name, key in self.keys[guild_id].items():
            for dungeon, level in key.items():
                keys += '\n{} ({}) - [{}]'.format(dungeon, level, name)

        if keys:
            embed.add_field(name='Current Keys', value=keys)

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
        self.keys[guild_id][name] = {
            DUNGEON_LIST[dungeon]: level
        }
        return self.generate_embed(guild_id)

    def remove_key(self, guild_id, name):
        self.check_cache()
        if name not in self.keys[str(guild_id)]:
            return {'content': 'No key found for \"{}\"'.format(name)}

        del self.keys[guild_id][name]
        return self.generate_embed(guild_id)

    def export_keys(self):
        with open('keys.json', 'w') as key_file:
            json.dump(self.keys, key_file)

    def import_keys(self):
        with open('keys.json', 'r') as f:
            data = json.load(f)
            self.keys = defaultdict(dict)
            self.keys.update(data)
