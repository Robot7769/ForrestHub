from sys import exit

from app.init import create_app, socketio
from app.utils import get_local_ip_address

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


PORT = 5000


def run_flask():
    app = create_app()
    socketio.run(
        app, host="0.0.0.0", port=PORT, use_reloader=False, debug=False
    )  # use_reloader=True, debug=True


if __name__ == "__main__":
    # stop the server with Ctrl-C
    try:
        local_ip = f"http://{get_local_ip_address()}:{PORT}"
        logger.debug(f"Server started at {local_ip}")
        run_flask()
    except KeyboardInterrupt:
        logger.debug("Server stopped")
        exit(0)
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
