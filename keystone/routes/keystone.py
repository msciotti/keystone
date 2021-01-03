from flask import Flask, request
from discord_interactions import verify_key_decorator, InteractionType
from utils.db_utils import upsert_keystone, remove_keystone, get_keystones_for_guild, register_user_with_guild
from utils.command_utils import options_to_dict, make_add_keystone_response, make_remove_keystone_response, make_list_keystone_response, make_generic_response

app = Flask(__name__)

@app.route('/keystone', methods=['POST'])
@verify_key_decorator('f569e0c182ea0d7a1db64c3e845ad4fcbf23c3f42837d1116d334a8f8b870641')
def keystone_interactions():
    if request.json['type'] == InteractionType.APPLICATION_COMMAND:
        request_data = request.json
        guild_id = request_data['guild_id']
        user_id = request_data['member']['user']['id']
        username = request_data['member']['user']['username'] + '#' + request_data['member']['user']['discriminator']
        command_data = request_data['data']
        command_options = {}
        args = {}

        if 'options' in command_data:
            command_options = request_data['data']['options']
            args = options_to_dict(command_options)

        register_user_with_guild(guild_id, user_id)
        
        if command_data['name'] == 'add':
            upsert_keystone(user_id, username, args['dungeon'], args['level'])
            return make_add_keystone_response()

        elif command_data['name'] == 'remove':
            remove_keystone(user_id)
            return make_remove_keystone_response()

        elif command_data['name'] == 'list':
            keystones = get_keystones_for_guild(guild_id)
            return make_list_keystone_response(keystones)
            
    return make_generic_response()