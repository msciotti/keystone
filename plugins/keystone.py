import requests
from disco.bot import Plugin
from disco.types.message import MessageTable, MessageEmbed


DUNGEON_LIST = {
  'seat': 'Seat of the Triumvirate',
  'brh': 'Black Rook Hold',
  'cos': 'Court of Stars',
  'dht': 'Darkheart Thicket',
  'eoa': 'Eye of Azshara',
  'hov': 'Halls of Valor',
  'mos': 'Maw of Souls',
  'nelth': 'Neltharion\'s Lair',
  'arc': 'The Arcway',
  'votw': 'Vault of the Wardens',
  'coen': 'Cathedral of Eternal Night',
  'lkara': 'Lower Return to Karazhan',
  'ukara': 'Upper Return to Karazhan'
}

KEYS = {}


def get_weekly_affix():
    r = requests.get('https://raider.io/api/v1/mythic-plus/affixes?region=us&locale=en')
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
                      url='https://github.com/msciotti/keystone',
                      icon_url='https://wow.zamimg.com/images/wow/icons/large/inv_relics_hourglass.jpg')
    embed.set_footer(text='Current Keystones',
                      icon_url='https://image.flaticon.com/icons/svg/25/25231.svg')
    return embed


class KeystonePlugin(Plugin):
    @Plugin.command('add', '<dungeon:str> <level:int> [character_name:str]')
    def on_keystone_add(self, event, dungeon, level, character_name=None):
        name = character_name or event.msg.author.username
        KEYS[name] = {
          DUNGEON_LIST[dungeon]: level
        }
        embed = generate_embed()
        return event.msg.reply(embed=embed)

    @Plugin.command('remove', '[character_name:str]')
    def on_keystone_remove(self, event, character_name=None):
        name = character_name or event.msg.author.username
        if KEYS[name]:
            del KEYS[name]
        else:
            event.msg.reply('No key was found for that name.')
        embed = generate_embed()
        return event.msg.reply(embed=embed)

    @Plugin.command('dungeons')
    def on_list_dungeons(self, event):
        tbl = MessageTable()
        tbl.set_header('Abbreviaton', 'Dungeon')
        for abv, name in DUNGEON_LIST.items():
            tbl.add(abv, name)
        return event.msg.reply(tbl.compile())

    @Plugin.command('list')
    def on_list_keys(self, event):
        embed = generate_embed()
        event.msg.reply(embed=embed)

    @Plugin.command('help')
    def on_help(self, event):
        tbl = MessageTable()
        tbl.set_header('Command', 'Description', 'Example')
        tbl.add('dungeons', 'list dungeon abbreviations')
        tbl.add('set', 'set a key with optional name', 'set hov 9 OR set hov 9 Simbra')
        tbl.add('remove', 'remove key with optional name', 'remove OR remove Simbra')
        tbl.add('list', 'list available dungeons')
        event.msg.reply(tbl.compile())
