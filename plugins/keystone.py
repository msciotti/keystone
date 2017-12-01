from disco.bot import Plugin
from disco.types.message import MessageTable
import helpers
from constants import DUNGEON_LIST


class KeystonePlugin(Plugin):
    @Plugin.command('add', '<dungeon:str> <level:int> [character_name:str]')
    def on_keystone_add(self, event, dungeon, level, character_name=None):
        name = character_name or event.msg.author.username
        key_list = helpers.add_key(name, level, dungeon)
        return event.msg.reply(embed=key_list)

    @Plugin.command('remove', '[character_name:str]')
    def on_keystone_remove(self, event, character_name=None):
        name = character_name or event.msg.author.username
        key_list = helpers.remove_key(name)
        return event.msg.reply(embed=key_list)

    @Plugin.command('list')
    def on_list_keys(self, event):
        key_list = helpers.list_keys
        return event.msg.reply(embed=key_list)

    @Plugin.command('dungeons')
    def on_list_dungeons(self, event):
        tbl = MessageTable()
        tbl.set_header('Abbreviaton', 'Dungeon')
        for abv, name in DUNGEON_LIST.items():
            tbl.add(abv, name)
        return event.msg.reply(tbl.compile())

    @Plugin.command('help')
    def on_help(self, event):
        tbl = MessageTable()
        tbl.set_header('Command', 'Description', 'Example')
        tbl.add('dungeons', 'list dungeon abbreviations')
        tbl.add('add', 'add a key with optional name',
                'set hov 9 OR set hov 9 Simbra')
        tbl.add('remove', 'remove key with optional name',
                'remove OR remove Simbra')
        tbl.add('list', 'list available dungeons')
        event.msg.reply(tbl.compile())
