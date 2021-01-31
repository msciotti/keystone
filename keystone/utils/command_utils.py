from flask import jsonify
from discord_interactions import InteractionResponseFlags, InteractionResponseType
from utils.db_utils import get_affixes


def options_to_dict(options):
        object_dict = {x['name']: x['value'] for x in options}
        return object_dict

def make_add_keystone_response():
    return jsonify({
        'type': InteractionResponseType.CHANNEL_MESSAGE,
        'data': {
            'content': 'Updated your keystone!',
            'flags': InteractionResponseFlags.EPHEMERAL
        }
    })

def make_remove_keystone_response():
    return jsonify({
        'type': InteractionResponseType.CHANNEL_MESSAGE,
        'data': {
            'content': 'Removed your keystone.',
            'flags': InteractionResponseFlags.EPHEMERAL
        }
    })

def make_list_keystone_response(keystones):
    characters = ''
    keys = ''
    levels = ''
    discord_users = ''
    affixes = get_affixes()

    # In order to get 3 lists with a Discord embed
    # We create 3 inline fields with values separated by newlines
    for users in keystones:
        print(users)
        for character in users:
            discord_users += f"{users[character]['username']}\n"
            characters += f"{users[character]['character']}\n"
            keys += f"{users[character]['dungeon']}\n"
            levels += f"{users[character]['level']}\n"
        
    return jsonify({
        'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        'data': {
            'content': ' ',
            'embeds': [
                {
                    'author': {
                        'name': 'Keystones',
                        'url': 'https://github.com/msciotti/keystone',
                        'icon_url': 'https://wow.zamimg.com/images/wow/icons/large/inv_relics_hourglass.jpg'
                    },
                    'fields': [
                        {
                            'name': 'Discord User',
                            'value': discord_users,
                            'inline': True
                        },
                        {
                            'name': 'Character',
                            'value': characters,
                            'inline': True
                        },
                        {
                            'name': 'Key',
                            'value': keys,
                            'inline': True
                        },
                        {
                            'name': 'Level',
                            'value': levels,
                            'inline': True
                        },
                        {
                            'name': f"{affixes[0]['name']} - (1+)",
                            'value': affixes[0]['description']
                        },
                        {
                            'name': f"{affixes[1]['name']} - (4+)",
                            'value': affixes[1]['description']
                        },
                        {
                            'name': f"{affixes[2]['name']} - (7+)",
                            'value': affixes[2]['description']
                        },
                        {
                            'name': f"{affixes[3]['name']} - (10+)",
                            'value': affixes[3]['description']
                        }
                    ]
                }
            ]       
        }
    })

def make_generic_response():
    return jsonify({
        'type': InteractionResponseType.CHANNEL_MESSAGE,
        'data': {
            'content': 'Command not found.',
            'flags': InteractionResponseFlags.EPHEMERAL
        }
    })