from flask import Blueprint
from ..controllers.server_member_controller import ServerMemberController

server_member_bp = Blueprint('server_member_bp', __name__)

server_member_bp.route('/<int:server_id>/members/<int:member_id>', methods=['GET'])(ServerMemberController.get)
server_member_bp.route('/<int:server_id>/members/<int:member_id>', methods=['DELETE'])(ServerMemberController.delete)

server_member_bp.route('/<int:server_id>/members', methods=['GET'])(ServerMemberController.get_all_by_server)
server_member_bp.route('/<int:server_id>/members', methods=['POST'])(ServerMemberController.create)


server_member_bp.route('/<int:server_id>/members/<int:member_id>', methods=['PUT'])(ServerMemberController.update)
