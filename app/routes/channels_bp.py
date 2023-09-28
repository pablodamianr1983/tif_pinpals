# cahnnels_bp
from flask import Blueprint
from ..controllers.channels_controller import ChannelsController

channels_bp = Blueprint('channels_bp', __name__)

channels_bp.route('/', methods=['GET'])(ChannelsController.get_all)
channels_bp.route('/<int:ID>', methods=['GET'])(ChannelsController.get)
channels_bp.route('/', methods=['POST'])(ChannelsController.create)
channels_bp.route('/<int:channel_id>', methods=['PUT'])(ChannelsController.update)
channels_bp.route('/<int:channel_id>', methods=['DELETE'])(ChannelsController.delete)
channels_bp.route('/by_server/<int:server_id>', methods=['GET'])(ChannelsController.get_by_server_id)
channels_bp.route('/by_server/<int:server_id>', methods=['GET'])(ChannelsController.get_by_server_id)
channels_bp.route('/<int:channel_id>/users', methods=['GET'])(ChannelsController.get_users_for_channel)


