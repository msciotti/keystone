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
    now = datetime.datetime.utcnow()

    # Get datetime of next Tuesday
    next_tuesday = now + datetime.timedelta(days=(1-now.weekday()) % 7)

    # It is Tuesday my dudes
    if now.weekday() is 1:
        one_week = datetime.timedelta(days=7)
        next_tuesday += one_week

    print next_tuesday
    # seconds_to_wait = (next_tuesday - now).total_seconds
    # t = Timer(seconds_to_wait, get_weekly_affix)
    # t.start()


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

    return {'embed': embed}


def add_key(name, level, dungeon, guild_id):
    if dungeon not in constants.DUNGEON_LIST:
        return {'content': '\"{}\" is not a valid dungeon. '
                'Please use `@keystone dungeons` for a list '
                'of valid dungeons.'.format(dungeon)}

    KEYS[guild_id][name] = {
        constants.DUNGEON_LIST[dungeon]: level
    }
    return generate_embed(guild_id)


def remove_key(name, guild_id):
    if name not in KEYS[guild_id]:
        return {'content': 'No key found for \"{}\"'.format(name)}

    del KEYS[guild_id][name]
    return generate_embed(guild_id)


def list_keys(guild_id):
    return generate_embed(guild_id)


def export_keys():
    with open('keys.json', 'w') as key_file:
        json.dumps(KEYS, key_file)
    return


def import_keys():
    with open('keys') as f:
        data = json.loads(f)
        print data
    return
