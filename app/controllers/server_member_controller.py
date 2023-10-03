# controllers/server_member_controller.py

from flask import jsonify, current_app

from ..models.server_member import ServerMember


class ServerMemberController:
    @classmethod
    def get(cls, server_id, member_id):
        member = ServerMember.get(server_id, member_id)
        if member is not None:
            return jsonify(member.serialize()), 200
        else:
            return jsonify({'message': 'Member not found'}), 404

    @classmethod
    def get_all_by_server(cls, server_id):
        members = ServerMember.get_all_by_server(server_id)
        return jsonify([member.serialize() for member in members]), 200

    @classmethod
    def create(cls, server_id, user_id):
        if not server_id or not user_id:
            return jsonify({'message': 'Invalid server ID or user ID'}), 400

        if ServerMember.get(server_id, user_id) is not None:
            return jsonify({'message': 'User is already a member of the server'}), 400

        member = ServerMember.create(server_id, user_id)
        return jsonify({'message': 'Member added to server successfully', 'member': member.serialize()}), 201

    @classmethod
    def delete(cls, server_id, user_id):
        member = ServerMember.get(server_id, user_id)
        if member is not None:
            ServerMember.delete(server_id, user_id)
            return jsonify({'message': 'Member removed from server successfully'}), 200
        else:
            return jsonify({'message': 'Error'}), 400

    @classmethod
    def update(cls, member_id, server_id, user_id):
        DatabaseConnection = current_app.config['DatabaseConnection']
        query = """UPDATE ServerMembers SET ServerID = %s, UserID = %s WHERE member_id = %s"""  # Cambio aquí
        params = (server_id, user_id, member_id)
        DatabaseConnection.execute_query(query, params=params)
