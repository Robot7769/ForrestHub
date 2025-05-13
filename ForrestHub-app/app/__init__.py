# from flask import Flask
# from flask_socketio import SocketIO
# from app.database import Database
# from config import Config
#
# socketio = SocketIO()
# db = Database()
#
#
# def create_app(debug=False):
#     app = Flask(__name__)
#     app.debug = debug
#     app.config.from_object(Config)
#
#     db.init_app(app)
#
#     from .routes import main as main_blueprint
#     app.register_blueprint(main_blueprint)
#
#     from .socketio_events import socketio_bp as socketio_blueprint
#     app.register_blueprint(socketio_blueprint)
#
#     from .api_routes import api_bp as api_blueprint  # New API blueprint
#     app.register_blueprint(api_blueprint)  # Register the new API blueprint
#
#     socketio.init_app(app)
#     return app
