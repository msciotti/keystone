from flask import jsonify
from discord_interactions import InteractionResponseFlags, InteractionResponseType


class CommandUtils():
    def options_to_dict(options):
        object_dict = {x.name: x.value for x in options}
        return object_dict

    def make_add_keystone_response():
        return jsonify({
            'type': InteractionResponseType.CHANNEL_MESSAGE,
            'data': {
                'content': 'Updated your keystone!',
                'flags': InteractionResponseFlags.Ephemeral
            }
        })

    def make_remove_keystone_response():
        return jsonify({
            'type': InteractionResponseType.CHANNEL_MESSAGE,
            'data': {
                'content': 'Removed your keystone.',
                'flags': InteractionResponseFlags.Ephemeral
            }
        })

    def make_list_keystone_response():
        return jsonify({
            'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {
                'content': 'Placeholder list'               
            }
        })

    def make_generic_response():
        return jsonify({
            'type': InteractionResponseType.CHANNEL_MESSAGE,
            'data': {
                'content': 'Command not found.',
                'flags': InteractionResponseFlags.Ephemeral
            }
        })