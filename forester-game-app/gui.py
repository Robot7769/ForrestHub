import tkinter as tk
from tkinter import messagebox

import socketio

# Connect to the Flask SocketIO server
sio = socketio.Client()


def send_notification():
    message = entry.get()
    if message:
        sio.emit("notification", {"message": message})
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a notification message")


def on_connect():
    print("Connected to the server")


def on_disconnect():
    print("Disconnected from the server")


def on_message(data):
    print("Message received:", data["message"])
    messagebox.showinfo("Notification", data["message"])


sio.on("connect", on_connect)
sio.on("disconnect", on_disconnect)
sio.on("message_to_gui", on_message)


def start_gui():
    sio.connect("http://localhost:5000/admin")

    global entry
    root = tk.Tk()
    root.title("Notification Sender")

    tk.Label(root, text="Enter Notification:").pack(pady=10)
    entry = tk.Entry(root, width=50)
    entry.pack(pady=10)

    send_button = tk.Button(root, text="Send Notification", command=send_notification)
    send_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    start_gui()
