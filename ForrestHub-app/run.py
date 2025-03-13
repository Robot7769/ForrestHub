import logging
import os
import sys
import webbrowser
import click
import eventlet
from datetime import datetime
from app.init import create_app, socketio
from config import Config
from pathlib import Path
from app.utils import is_port_free, find_free_port


logger = logging.getLogger(__name__)
__version__ = (Path(__file__).parent / "VERSION").read_text().strip()


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
        logger.info("Ukládám data...")
        eventlet.sleep(1)


def run_flask(config="config.Config", host="0.0.0.0", port=4444):
    app = create_app(config)
    socketio.run(
        app,
        host=host,
        port=port,
        use_reloader=False,
        debug=True,
    )


@click.command()
@click.option('--port', help='Port to run the server on')
@click.option('--host', help='Host address to bind the server')
@click.option('--host-qr', help='Host address shown in QR code in Admin panel')
@click.option('--version', is_flag=True, help='Show the version from setup.py')
def main(port, host, host_qr, version):
    config = Config()
    logger = setup_logging(config.EXECUTABLE_DIR, config.LOG_FOLDER)
    logging.basicConfig(level=logging.INFO)

    if version:
        print(f"ForrestHub App {__version__}")
        sys.exit(0)

    if port:
        config.PORT = port

    if host:
        config.HOST = host
        
    if host_qr:
        config.HOST_QR = host_qr

    if not is_port_free(config.HOST, config.PORT):
        new_port = find_free_port(config.HOST, 4444)
        logger.error(f"Port {config.PORT} is already in use, switching to next available port: {new_port}")
        config.PORT = new_port

    if config.FROZEN:
        webbrowser.open(f"http://{config.HOST}:{config.PORT}")
        webbrowser.open(f"http://{config.HOST}:{config.PORT}/admin")

    try:
        local_ip = f"http://{config.HOST}:{config.PORT}"
        print(f"Server started at {local_ip}")
        logger.info(f"Server started at {local_ip}")
        logger.info("Press Ctrl-C to stop the server")

        run_flask(config=config, host=config.HOST, port=config.PORT)
    except KeyboardInterrupt:
        logger.info("Server stopped")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
