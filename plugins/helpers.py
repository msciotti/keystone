import requests
from disco.types.message import MessageEmbed
import constants


KEYS = {}


def get_weekly_affix():
    r = requests.get(constants.AFFIX_URL)
    return r.json()


def generate_embed():
    embed = MessageEmbed()
    data = get_weekly_affix()
    keys = ''

    for name, key in KEYS.items():
        for dungeon, level in key.items():
            keys += '\n{} ({}) - [{}]'.format(dungeon, level, name)

    embed.add_field(name='Keys', value=keys)

    for affix in data['affix_details']:
        embed.add_field(name=affix['name'], value=affix['description'])

    embed.timestamp = '2017-11-28T23:42:41.752Z'
    embed.set_author(name='Mythic Keystones',
                     url=constants.GITHUB_URL,
                     icon_url=constants.KEYSTONE_ICON_URL)
    embed.set_footer(text='Current Keystones',
                     icon_url=constants.GITHUB_ICON_URL)
    print embed
    return embed


def add_key(name, level, dungeon):
    KEYS[name] = {
        constants.DUNGEON_LIST[dungeon]: level
    }
    return generate_embed()


def remove_key(name):
    if name in KEYS:
        del KEYS[name]
    return generate_embed()


def list_keys():
    return generate_embed()
