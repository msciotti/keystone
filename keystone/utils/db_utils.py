import sqlite3

connection = sqlite3.connect("../data/keystone.db")
cursor = connection.cursor()

class DBUtils():
    def upsert_keystone(user_id, username, dungeon, level):
        query = """
            REPLACE INTO keystones
            SET
                user_id = ?,
                username = ?,
                dungeon = ?,
                level = ?
        """
        cursor.execute(query, (user_id, username, dungeon, level))

    def remove_keystone(user_id):
        query = """
            DELETE FROM keystones
            WHERE user_id = ?
        """
        cursor.execute(query, (user_id))

    def get_keystones_for_guild(guild_id):
        query = """
            SELECT username, dungeon, level
            FROM keystones k
            JOIN user_guild_map u
            ON k.user_id = u.user_id
            WHERE u.guild_id = ?
        """

        rows = cursor.execute(query, (guild_id)).fetchall()
        return rows

    def register_user_with_guild(guild_id, user_id):
        query = """
            INSERT OR IGNORE INTO user_guild_map
            SET
                guild_id = ?,
                user_id = ?,
                unique_id = ?
        """
        
        cursor.execute(query, (guild_id, user_id, guild_id + user_id))