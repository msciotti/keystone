from disco.bot import Plugin
from disco.types.message import MessageTable
from keystone_storage import KeystoneStorage
from constants import DUNGEON_LIST


@Plugin.with_config(KeystoneStorage)
class KeystonePlugin(Plugin):
    def load(self, ctx):
        super(KeystonePlugin, self).load(ctx)
        self.keys = KeystoneStorage()
        self.keys.cache()

    @Plugin.command('add', '<dungeon:str> <level:int> [character_name:str...]')
    def on_keystone_add(self, event, dungeon, level, character_name=None):
        name = character_name or event.msg.author.username
        return event.msg.reply(
            **self.keys.add_key(str(event.msg.guild.id), name, dungeon, level)
            )

    @Plugin.command('remove', '[character_name:str...]')
    def on_keystone_remove(self, event, character_name=None):
        name = character_name or event.msg.author.username
        return event.msg.reply(
            **self.keys.remove_key(str(event.msg.guild.id), name)
            )

    @Plugin.command('list')
    def on_list_keys(self, event):
        return event.msg.reply(
            **self.keys.generate_embed(str(event.msg.guild.id))
            )

    @Plugin.command('dungeons')
    def on_list_dungeons(self, event):
        tbl = MessageTable()
        tbl.set_header('Abbreviaton', 'Dungeon')
        for abv, name in DUNGEON_LIST.items():
            tbl.add(abv, name)
        return event.msg.reply(tbl.compile())

    @Plugin.command('export')
    def on_keys_export(self, event):
        # Admin abuse - set to your id
        if event.msg.author.id != 53908232506183680:
            return event.msg.reply('Not authorized to use this command.')

        self.keys.export_keys()
        return event.msg.reply('Exported keys!')

    @Plugin.command('import')
    def on_keys_import(self, event):
        # Admin abuse - set to your id
        if event.msg.author.id != 53908232506183680:
            return event.msg.reply('Not authorized to use this command.')

        self.keys.import_keys()
        return event.msg.reply('Imported keys!')

    @Plugin.command('help')
    def on_help(self, event):
        tbl = MessageTable()
        tbl.set_header('Command', 'Description', 'Example')
        tbl.add('dungeons', 'list dungeon abbreviations', '')
        tbl.add('add', 'add a key with optional name',
                'set hov 9 OR set hov 9 Simbra')
        tbl.add('remove', 'remove key with optional name',
                'remove OR remove Simbra')
        tbl.add('list', 'list available dungeons', '')
        tbl.add('export', 'exports existing keys to a file', '')
        tbl.add('import', 'imports previously exported keys', '')
        event.msg.reply(tbl.compile())
