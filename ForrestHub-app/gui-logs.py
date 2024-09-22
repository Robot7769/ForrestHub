import logging
import queue
import sys
import tkinter as tk
from threading import Thread
from tkinter import scrolledtext as st

from run import run_flask, setup_logging


# https://chatgpt.com/c/90e8941e-62f4-4fd0-bf1d-0b79dc6d22c1


class CustomStream:
    def __init__(self, original_stream, log_queue):
        self.original_stream = original_stream
        self.log_queue = log_queue

    def write(self, message):
        self.log_queue.put((message, logging.INFO))
        self.original_stream.write(message)
        self.original_stream.flush()

    def flush(self):
        self.original_stream.flush()


class LogHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        log_entry = self.format(record)
        self.log_queue.put((log_entry, record.levelno))
        print(log_entry)  # Also print to the terminal


class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flask Logs")

        self.text_area = st.ScrolledText(self.root, font=("Times New Roman", 12))
        self.text_area.grid(row=0, column=0, sticky="nsew")
        self.text_area.configure(state="disabled")

        # Define tags for different log levels
        self.text_area.tag_configure("INFO", foreground="black")
        self.text_area.tag_configure("WARNING", foreground="orange")
        self.text_area.tag_configure("ERROR", foreground="red")
        self.text_area.tag_configure("CRITICAL", foreground="red", background="yellow")

        self.log_queue = queue.Queue()
        self.log_handler = LogHandler(self.log_queue)
        self.log_handler.setLevel(logging.INFO)  # Set level to INFO
        self.log_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logging.getLogger().addHandler(self.log_handler)

        self.update_logs()

        # Make the grid expand to fit the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Schedule the Flask server to start after 3 seconds
        self.root.after(3000, self.start_flask_app)

    def update_logs(self):
        while not self.log_queue.empty():
            log_message, levelno = self.log_queue.get()
            self.text_area.configure(state="normal")
            if levelno == logging.INFO:
                self.text_area.insert(tk.END, log_message + "\n", "INFO")
            elif levelno == logging.WARNING:
                self.text_area.insert(tk.END, log_message + "\n", "WARNING")
            elif levelno == logging.ERROR:
                self.text_area.insert(tk.END, log_message + "\n", "ERROR")
            elif levelno == logging.CRITICAL:
                self.text_area.insert(tk.END, log_message + "\n", "CRITICAL")
            self.text_area.configure(state="disabled")
            self.text_area.see(tk.END)
        self.root.after(100, self.update_logs)

    def start_flask_app(self):
        flask_thread = Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()


def main():
    setup_logging()  # Setup logging before starting the GUI and Flask app
    root = tk.Tk()
    app = GUIApp(root)

    # Redirect stdout and stderr
    sys.stdout = CustomStream(sys.stdout, app.log_queue)
    sys.stderr = CustomStream(sys.stderr, app.log_queue)

    root.mainloop()


if __name__ == "__main__":
    main()
