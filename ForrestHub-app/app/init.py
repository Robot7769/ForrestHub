from app.custom_loader import CustomLoader
from app.database import Database
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")
db = Database()


def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    db.init(app.config["EXECUTABLE_DIR"], app.config["DATAFILE"])

    # Set custom Jinja loader

    loader_locations = [
        app.config.get("GAMES_FOLDER"),
        app.config.get("TEMPLATES_FOLDER"),
        app.config.get("ASSETS_FOLDER"),
        app.config.get("PAGES_FOLDER"),
    ]

    if app.config.get("LIVE_GAMES_MODE"):
        loader_locations.append(app.config.get("GAMES_FOLDER_LIVE"))

    app.jinja_loader = CustomLoader(loader_locations)

    # Register Blueprints
    from app.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from app.errors import errors as errors_blueprint

    app.register_blueprint(errors_blueprint)

    # Import and register SocketIO events
    from app.socketio_events import socketio_bp as socketio_blueprint

    app.register_blueprint(socketio_blueprint)

    # Initialize SocketIO
    socketio.init_app(app)

    return app
