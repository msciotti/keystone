from disco.bot import Plugin
from disco.types.message import MessageTable
import helpers
from constants import DUNGEON_LIST


helpers.get_weekly_affix()


class KeystonePlugin(Plugin):
    @Plugin.command('add', '<dungeon:str> <level:int> [character_name:str]')
    def on_keystone_add(self, event, dungeon, level, character_name=None):
        name = character_name or event.msg.author.username
        msg_guild = event.msg.guild
        guild_id = msg_guild.id
        key_list = helpers.add_key(name, level, dungeon, guild_id)
        return event.msg.reply(embed=key_list)

    @Plugin.command('remove', '[character_name:str]')
    def on_keystone_remove(self, event, character_name=None):
        name = character_name or event.msg.author.username
        msg_guild = event.msg.guild
        guild_id = msg_guild.id
        key_list = helpers.remove_key(name, guild_id)
        return event.msg.reply(embed=key_list)

    @Plugin.command('list')
    def on_list_keys(self, event):
        msg_guild = event.msg.guild
        guild_id = msg_guild.id
        key_list = helpers.list_keys(guild_id)
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
