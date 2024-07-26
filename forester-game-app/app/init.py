from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from app.custom_loader import CustomLoader
from app.database import Database
import os

socketio = SocketIO(cors_allowed_origins="*")
db = Database()


def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    db.init(app.config["ROOT_DIR"], app.config["DATAFILE"])

    # Set custom Jinja loader
    root_path = app.config["ROOT_DIR"]
    app.jinja_loader = CustomLoader(
        [os.path.join(root_path, "pages"), os.path.join(root_path, "templates")]
    )

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
