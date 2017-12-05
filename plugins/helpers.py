import requests
import datetime
import json
from collections import defaultdict
from disco.types.message import MessageEmbed
from threading import Timer
import constants


KEYS = defaultdict(dict)
AFFIXES = {}


def get_weekly_affix():
    'Getting new data...'
    r = requests.get(constants.AFFIX_URL, timeout=2)
    global AFFIXES
    AFFIXES = r.json()
    print 'Got data:'
    print json.dumps(AFFIXES, indent=4)
    global KEYS
    KEYS = defaultdict(dict)
    cache()


def cache():
    print 'Caching...'
    d = datetime.datetime.now()
    reset = d + datetime.timedelta(days=(1-d.weekday() + 7) % 7)
    reset = reset.replace(hour=16, minute=0, second=0, microsecond=0)
    print 'Will reset data on {}'.format(reset)
    seconds_to_wait = (reset - d).total_seconds()
    t = Timer(seconds_to_wait, get_weekly_affix)
    t.start()


def generate_embed(guild_id):
    embed = MessageEmbed()
    keys = ''

    for name, key in KEYS[guild_id].items():
        for dungeon, level in key.items():
            keys += '\n{} ({}) - [{}]'.format(dungeon, level, name)

    if keys:
        embed.add_field(name='Current Keys', value=keys)

    for affix in AFFIXES['affix_details']:
        embed.add_field(name=affix['name'], value=affix['description'])

    embed.set_author(name='Mythic Keystones',
                     url=constants.GITHUB_URL,
                     icon_url=constants.KEYSTONE_ICON_URL)

    print embed
    return embed


def add_key(name, level, dungeon, guild_id):
    KEYS[guild_id][name] = {
        constants.DUNGEON_LIST[dungeon]: level
    }
    return generate_embed(guild_id)


def remove_key(name, guild_id):
    if name in KEYS[guild_id]:
        del KEYS[guild_id][name]
    return generate_embed(guild_id)


def list_keys(guild_id):
    return generate_embed(guild_id)
