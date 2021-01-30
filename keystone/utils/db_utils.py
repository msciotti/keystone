import sqlite3
import redis
import json
import requests
import datetime
import math
from os.path import dirname, abspath, join
from datetime import datetime, timedelta

r = redis.Redis()

path = dirname(dirname(abspath(__file__)))
db = join(path, 'data/keystone.db')
connection = sqlite3.connect(db, check_same_thread=False)
cursor = connection.cursor()

def get_seconds_to_reset():
    today = datetime.today()
    tuesday = today + timedelta((1-today.weekday()) % 7)
    
    # total_seconds() returns a float and we just need an int for redis
    ttl = math.floor((tuesday-today).total_seconds())

    # If today is tuesday, hardcode to 1 week
    if ttl == 0:
        ttl = 604800

    return ttl


def upsert_keystone(user_id, username, dungeon, level, character=None):
    # Our data structure in Redis looks like:
    # {
    #   user_id: {
    #       character_name {
    #           keystone_object
    #       }        
    #   }
    # }
    keystone = {
        'username': username,
        'dungeon': dungeon,
        'level': level,
        'character': character
    }

    ttl = get_seconds_to_reset()
    current_keystones = r.get(user_id)
    current_keystones = json.loads(current_keystones)
    current_keystones[character] = keystone
    r.setex(user_id, ttl, json.dumps(current_keystones))

def remove_keystone(user_id):
    r.delete(user_id)

def get_keystones_for_guild(guild_id):
    # We need to get the list of users from sqlite3 for the guild
    # Then we can pull the matching keystones from redis
    keystones = []
    query = '''
        SELECT user_id
        FROM user_guild_map
        WHERE guild_id = ?
    '''

    rows = cursor.execute(query, (guild_id, )).fetchall()
    user_ids = rows[0]
    for id in user_ids:
        keystone = r.get(id)
        # keystone is a json string here
        # We want to make it a dict
        keystones.append(json.loads(keystone))

    return keystones

def register_user_with_guild(guild_id, user_id):
    # We use sqlite3 here because we need a relational database
    # We need to get all users who are registered with a given guild_id
    unique_id = guild_id + user_id
    query = '''
        INSERT OR IGNORE INTO user_guild_map (guild_id, user_id, unique_id)
        VALUES (?, ?, ?)
    '''
    
    cursor.execute(query, (guild_id, user_id, unique_id))
    connection.commit()

def get_affixes():
    affixes = r.get('affixes_us')

    if affixes is None:
        # Get weekly affixes from raider.io
        affixes = []
        request = requests.get('https://raider.io/api/v1/mythic-plus/affixes?region=us')
        response_json = request.json()

        for affix in response_json['affix_details']:
            affixes.append({
                "name": affix['name'],
                "description": affix['description']
            })

        ttl = get_seconds_to_reset()
        r.setex('affixes_us', ttl, json.dumps(affixes))

    # affixes is a json string when read out of redis
    return json.loads(affixes)