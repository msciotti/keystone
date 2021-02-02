import requests
import re
import os
from flask import Flask, request
from flask_cors import CORS
from discord_interactions import verify_key_decorator, InteractionType
from utils.db_utils import upsert_keystone, remove_keystone, get_keystones_for_guild, register_user_with_guild
from utils.command_utils import options_to_dict, make_add_keystone_response, make_remove_keystone_response, make_list_keystone_response, make_generic_response

app = Flask(__name__)
CORS(app)

@app.route('/keystone', methods=['POST'])
@verify_key_decorator(os.environ.get('KEYSTONE_PUBLIC_KEY'))
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

        elif command_data['name'] == 'keys':
            keystones = get_keystones_for_guild(guild_id)
            return make_list_keystone_response(keystones)
            
    return make_generic_response()

@app.route('/token', methods=['POST'])
def handle_oauth2_redirect():
    code = request.json['code']
    if code is None:
        return 'Could not get code', 400

    data = {
        'code': code,
        'client_id': os.environ.get('KEYSTONE_CLIENT_ID'),
        'client_secret': os.environ.get('KEYSTONE_CLIENT_SECRET'),
        'redirect_uri': 'https://keystone.masonsciotti.com/callback',
        'grant_type': 'authorization_code',
        'scope': 'identify'
    }

    r = requests.post('https://discord.com/api/v8/oauth2/token', data=data)
    r.raise_for_status()
    return r.json()

@app.route('/update-keystones', methods=['POST'])
def update_keystones_from_companion_app():
    character = request.json['character']
    username = request.json['username']
    user_id = request.json['user_id']
    key_data = request.json['key_data']

    # Regex matching the format DungeonName: (Level)
    contents_search = re.search(r'(?:Keystone: )((?:[a-zA-z]+\s{0,1})+)\s(?:\((\d+)\))', key_data)
    if not contents_search:
        return 'Could not get keystone', 400

    dungeon = contents_search.group(1)
    level = contents_search.group(2)
    upsert_keystone(user_id, username, dungeon, level, character)
    return 'Keystone saved'

