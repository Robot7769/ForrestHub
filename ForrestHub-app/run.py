import logging
import os
import sys
import webbrowser
import eventlet
import eventlet.green.threading as threading
from datetime import datetime

from app.init import create_app, socketio
from config import Config

logger = logging.getLogger(__name__)


def setup_logging(root_dir: str, log_folder: str = "ForrestHubLogs"):
    logs_dir = os.path.join(root_dir, log_folder)
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(
        logs_dir, f'ForrestHub_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    return logging.getLogger(__name__)


def save_data_periodically():
    while True:
        # Simulace ukládání dat každou vteřinu
        logger.info("Ukládám data...")
        eventlet.sleep(1)


def run_flask(config="config.Config"):
    app = create_app(config)

    socketio.run(
        app,
        host="0.0.0.0",
        port=app.config["PORT"],
        use_reloader=False,
        debug=True,
    )


if __name__ == "__main__":
    config = Config()

    if len(sys.argv) > 1:
        config.PORT = int(sys.argv[1])

    logger = setup_logging(config.EXECUTABLE_DIR, config.LOG_FOLDER)
    logging.basicConfig(level=logging.INFO)

    if config.FROZEN:
        webbrowser.open(f"http://{config.IP_ADDRESS}:{config.PORT}")
        webbrowser.open(f"http://{config.IP_ADDRESS}:{config.PORT}/admin")

    try:
        local_ip = f"http://{config.IP_ADDRESS}:{config.PORT}"
        print(f"Server started at {local_ip}")
        logger.info(f"Server started at {local_ip}")
        logger.info("Press Ctrl-C to stop the server")

        run_flask(config=config)
    except KeyboardInterrupt:
        logger.info("Server stopped")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        sys.exit(1)
