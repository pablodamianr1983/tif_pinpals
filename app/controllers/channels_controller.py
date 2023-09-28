# channels_controller.py
from flask import request, jsonify

from .. import Users
from ..models.channels import Channels
from ..models.exceptions import ChannelNotFound
from ..models.messages import Messages


class ChannelsController:
    @classmethod
    def get(cls, ID):
        channel = Channels(ID=ID)
        result = Channels.get(channel)
        if result is not None:
            return result.serialize(), 200
        else:
            raise ChannelNotFound(ID)

    @classmethod
    def get_all(cls):
        channel_objects = Channels.get_all()
        channels = []
        for channel in channel_objects:
            channels.append(channel.serialize())
        return channels, 200

    @classmethod
    def create(cls):
        data = request.json
        channel = Channels(**data)
        Channels.create(channel)
        return {'message': 'Channel created successfully'}, 201

    @classmethod
    def update(cls, ID):
        data = request.json
        data['ID'] = ID
        channel = Channels(**data)
        Channels.update(channel)
        return {'message': 'Channel updated successfully'}, 200

    @classmethod
    def delete(cls, channel_id):
        channel = Channels(ID=channel_id)
        Channels.delete(channel)
        return {'message': 'Channel deleted successfully'}, 204

    @classmethod
    def get_channels_by_server_id(cls, server_id):
        return Channels.get_by_server_id(server_id)

    @classmethod
    def get_by_server_id(cls, server_id):
        channels = Channels.get_by_server_id(server_id)
        if channels:
            return jsonify([channel.serialize() for channel in channels]), 200
        else:
            return jsonify({"message": "No channels found for the provided server ID"}), 400

    @classmethod
    def get_users_for_channel(cls, channel_id):
        user_ids = Messages.get_unique_users_for_channel(channel_id)
        users = [Users.get_by_user_id(user_id) for user_id in user_ids]
        return jsonify([user.serialize() for user in users])
