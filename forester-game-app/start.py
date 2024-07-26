import multiprocessing
import time
import webbrowser

from gui import start_gui
from run import run_flask

if __name__ == "__main__":
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()
    time.sleep(2)  # Wait for the Flask server to start
    webbrowser.open('http://localhost:5000')  # Optionally open the browser automatically
    start_gui()
    flask_process.join()
