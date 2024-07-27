import logging
import os
import sys
import webbrowser
from datetime import datetime

from app.init import create_app, socketio
from config import Config

logger = logging.getLogger(__name__)


def setup_logging(root_dir: str, log_folder: str = "ForesterLogs"):
    # Create a logs directory if it doesn't exist
    logs_dir = os.path.join(root_dir, log_folder)
    os.makedirs(logs_dir, exist_ok=True)

    # Create a log file name with a timestamp
    log_file = os.path.join(
        logs_dir, f'Forester_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )

    # Set up logging to file
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    return logging.getLogger(__name__)


def run_flask():
    app = create_app()
    socketio.run(
        app,
        host="0.0.0.0",
        port=app.config["PORT"],
        use_reloader=app.config["USE_RELOADER"],
        debug=app.config["DEBUG"],
    )


if __name__ == "__main__":
    config = Config()

    logger = setup_logging(config.ROOT_DIR, config.LOG_FOLDER)
    logging.basicConfig(level=logging.INFO)

    if not config.DEBUG:
        webbrowser.open(f"http://{config.IP_ADDRESS}:{config.PORT}")
        webbrowser.open(f"http://{config.IP_ADDRESS}:{config.PORT}/admin")

    try:
        local_ip = f"http://{config.IP_ADDRESS}:{config.PORT}"
        print(f"Server started at {local_ip}")
        logger.info(f"Server started at {local_ip}")
        logger.info("Press Ctrl-C to stop the server")
        run_flask()
    except KeyboardInterrupt:
        logger.info("Server stopped")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        sys.exit(1)
