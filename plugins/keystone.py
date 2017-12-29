from disco.bot import Plugin
from disco.types.message import MessageTable
import helpers
from constants import DUNGEON_LIST


helpers.get_weekly_affix()


class KeystonePlugin(Plugin):
    @Plugin.command('add', '<dungeon:str> <level:int> [character_name:str...]')
    def on_keystone_add(self, event, dungeon, level, character_name=None):
        name = character_name or event.msg.author.username
        msg_guild = event.msg.guild
        guild_id = msg_guild.id
        response = helpers.add_key(name, level, dungeon, guild_id)
        return event.msg.reply(**response)

    @Plugin.command('remove', '[character_name:str...]')
    def on_keystone_remove(self, event, character_name=None):
        name = character_name or event.msg.author.username
        msg_guild = event.msg.guild
        guild_id = msg_guild.id
        response = helpers.remove_key(name, guild_id)
        return event.msg.reply(**response)

    @Plugin.command('list')
    def on_list_keys(self, event):
        msg_guild = event.msg.guild
        guild_id = msg_guild.id
        response = helpers.list_keys(guild_id)
        return event.msg.reply(**response)

    @Plugin.command('dungeons')
    def on_list_dungeons(self, event):
        tbl = MessageTable()
        tbl.set_header('Abbreviaton', 'Dungeon')
        for abv, name in DUNGEON_LIST.items():
            tbl.add(abv, name)
        return event.msg.reply(tbl.compile())

    @Plugin.command('export')
    def on_keys_export(self, event):
        # Admin abuse
        if event.msg.author.id != 53908232506183680:
            return event.msg.reply('You are not authorized to use this command.')

        helpers.export_keys()
        return event.msg.reply('Exported keys!')

    @Plugin.command('import')
    def on_keys_import(self, event):
        # Admin abuse
        if event.msg.author.id != 53908232506183680:
            return event.msg.reply('You are not authorized to use this command.')

        helpers.import_keys()
        return event.msg.reply('Imported keys!')

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
