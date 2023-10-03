# users_controller.py
from flask import request, session, jsonify

from ..models.exceptions import UserNotFound
from ..models.users import Users


class UsersController:
    @classmethod
    def get(cls, user_id):
        user = Users(ID=user_id)
        result = Users.get(user)
        if result is not None:
            return result.serialize(), 200
        else:
            raise UserNotFound(user_id)

    @classmethod
    def get_all(cls):
        user_objects = Users.get_all()
        users = []
        for user in user_objects:
            users.append(user.serialize())
        return users, 200

    @classmethod
    def create(cls):
        data = request.json
        user = Users(**data)
        Users.create(user)
        return {'message': 'User created successfully'}, 201

    @classmethod
    def update(cls, user_id):
        data = request.json
        data['ID'] = user_id
        user = Users(**data)
        Users.update(user)
        return {'message': 'User updated successfully'}, 200

    @classmethod
    def delete(cls, ID):
        user = Users(ID=ID)
        Users.delete(user)
        return {'message': 'User deleted successfully'}, 204

    @classmethod
    def login(cls, username, password):
        user = Users.get_by_username(username)
        if user and user.check_password(password):
            session['username'] = user.Username
            session['id'] = user.ID
            return jsonify({'success': True, 'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
