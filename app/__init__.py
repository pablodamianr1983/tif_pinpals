# __init__
from flask import Flask, request, jsonify, session
from flask_cors import CORS

from config import Config
from .database import DatabaseConnection
from .models.servers import Servers
from .models.users import Users
from .routes.auth_bp import auth_bp
from .routes.channels_bp import channels_bp
from .routes.error_handlers import errors
from .routes.messages_bp import messages_bp
from .routes.server_members_bp import server_member_bp
from .routes.servers_bp import servers_bp
from .routes.users_bp import users_bp


def init_app():
    """Crea y configura la aplicación Flask"""

    app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)

    CORS(app, supports_credentials=True)
    CORS(app, resources={r"/server-members/*": {"origins": "http://127.0.0.1:5000"}})
    CORS(server_member_bp, methods=["GET", "POST", "PUT", "DELETE"])

    app.config.from_object(
        Config
    )

    DatabaseConnection.set_config(app.config)
    app.config['DatabaseConnection'] = DatabaseConnection()
    app.config['Servers'] = Servers
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(servers_bp, url_prefix='/servers')
    app.register_blueprint(channels_bp, url_prefix='/channels')
    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(errors)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(server_member_bp, url_prefix='/server-members')

    @app.route('/server-members', methods=['OPTIONS'])
    def options_server_members():
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # Registra las rutas de server_member_bp y otros blueprints aquí

    if __name__ == "__main__":
        app.run(host='127.0.0.1', port=5000)

    @app.route('/servers/search', methods=['GET'])
    def search_servers():
        term = request.args.get('term', default="", type=str)
        criteria = request.args.get('criteria', default="name", type=str)

        servers = Servers.search(term, criteria)
        return jsonify([server.serialize() for server in servers])

    @app.route('/userdata', methods=['GET'])
    def get_user_data():

        if 'user_id' in session:
            user = Users.get_by_user_id(session['user_id'])
            user_data = {
                'username': user.Username,
                'email': user.Email
            }
            return jsonify(user_data)
        else:
            app.logger.warning("Usuario no autenticado intentó acceder a /userdata")
            return jsonify({'error': 'Usuario no autenticado'})

    return app
