from flask import Flask, request

from discord_interactions import verify_key_decorator, InteractionType
from keystone.utils.command_utils import CommandUtils
from keystone.utils.db_utils import DBUtils

app = Flask(__name__)

@app.route('/keystone', methods=['POST'])
@verify_key_decorator('f569e0c182ea0d7a1db64c3e845ad4fcbf23c3f42837d1116d334a8f8b870641')
def keystone_interactions():
    if request.json['type'] == InteractionType.APPLICATION_COMMAND:
        request_data = request.json['data']
        guild_id = request_data['guild_id']
        user_id = request_data['member']['user']['id']
        username = request_data['member']['user']['username'] + '#' + request_data['member']['user']['discriminator'] 

        DBUtils.register_user_with_guild(guild_id, user_id)

        if request_data['options'] is not None:
            args = CommandUtils.options_to_dict(request_data['options'])
        
        if request_data['name'] == 'add':
            add_keystone(user_id, username, args['dungeon'], args['level'])
            return CommandUtils.make_add_keystone_response()

        elif request_data['name'] == 'remove':
            remove_keystone(user_id)
            return CommandUtils.make_keystone_remove_response()

        elif request_data['name'] == 'list':
            keystones = list_keystones_for_guild(guild_id)
            return CommandUtils.make_keystone_list_response(keystones)
            
    return CommandUtils.make_generic_response()

def add_keystone(user_id, username, dungeon, level):
    DBUtils.upsert_keystone(user_id, username, dungeon, level)

def remove_keystone(user_id):
    DBUtils.remove_keystone(user_id)

def list_keystones_for_guild(guild_id):
    keystones = DBUtils.get_keystones_for_guild(guild_id)
    return keystones