# models/server_member.py

from flask import current_app


class ServerMember:
    def __init__(self, ServerID, UserID):
        self.ServerID = ServerID  
        self.UserID = UserID

    def serialize(self):
        return {
            "ServerID": self.ServerID,
            "UserID": self.UserID,}

    def save(self):
        DatabaseConnection = current_app.config['DatabaseConnection']
        query = """INSERT INTO ServerMembers (ServerID, UserID) VALUES (%s, %s) ON DUPLICATE KEY UPDATE ServerID = 
        VALUES(ServerID), UserID = VALUES(UserID) """
        params = (self.ServerID, self.UserID)
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def get(cls, server_id, user_id):
        DatabaseConnection = current_app.config['DatabaseConnection']
        query = """SELECT ServerID, UserID FROM ServerMembers WHERE ServerID = %s AND UserID = %s"""
        params = (server_id, user_id)
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return cls(*result)
        return None

    @classmethod
    def get_all_by_server(cls, server_id):
        DatabaseConnection = current_app.config['DatabaseConnection']
        query = """SELECT ServerID, UserID FROM ServerMembers WHERE ServerID = %s"""
        params = (server_id,)
        results = DatabaseConnection.fetch_all(query, params=params)

        members = []
        if results is not None:
            for result in results:
                members.append(cls(*result))
        return members

    @classmethod
    def create(cls, server_id, user_id):
        existing_member = cls.get(server_id, user_id)
        if existing_member:
            return None, 'Member already exists'

        DatabaseConnection = current_app.config['DatabaseConnection']
        query = """INSERT INTO ServerMembers (ServerID, UserID) VALUES (%s, %s)"""
        params = (server_id, user_id)

        try:
            DatabaseConnection.execute_query(query, params=params)
            return cls(server_id, user_id), 'Member added successfully'
        except Exception as e:
            print(e)
            return None, 'Failed to add member'

    @classmethod
    def delete(cls, server_id, user_id):
        DatabaseConnection = current_app.config['DatabaseConnection']
        query = """DELETE FROM ServerMembers WHERE ServerID = %s AND UserID = %s"""
        params = (server_id, user_id)
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def update(cls, member_id, server_id, user_id):
        DatabaseConnection = current_app.config['DatabaseConnection']
        query = """UPDATE ServerMembers SET ServerID = %s, UserID = %s WHERE member_id = %s"""
        params = (server_id, user_id, member_id)
        DatabaseConnection.execute_query(query, params=params)
        return cls(server_id, user_id)
