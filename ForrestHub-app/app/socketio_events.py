from flask import Blueprint
from flask_socketio import emit

from app.init import socketio, db

from flask import (
    Blueprint,
    render_template,
    abort,
    send_from_directory,
    current_app,
    jsonify,
    request,
)

socketio_bp = Blueprint("socketio", __name__)
connected_clients = 0
connected_admins = 0



game_status = "running"


@socketio.on("send_admin_message")
def handle_admin_message(message):
    emit("admin_messages", message, broadcast=True)


@socketio.on("connect")
def handle_connect():
    global connected_clients
    connected_clients += 1
    emit("update_clients", {"count": connected_clients}, broadcast=True)


@socketio.on("disconnect")
def handle_disconnect():
    global connected_clients
    connected_clients -= 1
    emit("update_clients", {"count": connected_clients}, broadcast=True)


@socketio.on("get_game_status")
def handle_game_status(demo):
    global game_status
    emit("game_status", game_status)


@socketio.on("set_game_status")
def handle_set_game_status(status: str):
    global game_status
    game_status = status
    emit("game_status", game_status, broadcast=True)


@socketio.on("get_all_db")
def handle_get_all_data(data) -> dict:
    return {"status": "ok", "data": db.get_data()}


@socketio.on("delete_all_db")
def handle_delete_all_data(data) -> dict:
    db.overwrite_data_dict({})
    return {"status": "ok"}


@socketio.on("set_key")
def handle_set_key(json: dict):
    key = json.get("key")
    value = json.get("value")
    db.set_data_key(key, value)
    return {"status": "ok"}


@socketio.on("set_key_broadcast")
def handle_set_key_broadcast(json: dict):
    key = json.get("key")
    value = json.get("value")
    db.set_data_key(key, value)
    emit(key, value, broadcast=True)
    return {"status": "ok"}


@socketio.on("exists_key")
def handle_exists_key(key: str) -> dict:
    return {"status": "ok", "exists": db.get_data_key(key) is not None}


@socketio.on("get_key")
def handle_get_key(json: dict) -> dict:
    key = json.get("key")
    default_value = json.get("defaultValue")
    return {"status": "ok", "data": db.get_data_key(key, default_value)}


@socketio.on("delete_key")
def handle_delete_key(key: str) -> dict:
    db.delete_data_key(key)
    return {"status": "ok"}


# add_new_game - create folder with game name
@socketio.on("add_new_game")
def handle_add_new_game(game_name: str) -> dict:
    game_folder = current_app.config.get("GAMES_FOLDER")
    if not game_folder:
        return {"status": "error", "message": "No live data folder"}

    game_folder = game_folder / game_name

    if game_folder.exists():
        return {"status": "error", "message": "Game already exists"}
    game_folder.mkdir()
    return {"status": "ok"}



# add_new_game_page - create new page in game folder
@socketio.on("add_new_game_page")
def handle_add_new_game_page(json: dict) -> dict:
    game_name = json.get("game")
    game_page = json.get("page")
    page_content = json.get("content")


    game_folder = current_app.config.get("GAMES_FOLDER_LIVE")
    if not game_folder:
        return {"status": "error", "message": "No live data folder"}

    game_folder = game_folder / game_name

    if not game_folder.exists():
        game_folder.mkdir()

    page_path = game_folder / f"{game_page}.html"
    if page_path.exists():
        return {"status": "error", "message": "Page already exists"}

    with open(page_path, "w") as f:
        f.write(page_content)
    return {"status": "ok"}

# get_page_html - get html content of page
@socketio.on("get_page_html")
def handle_get_page_html(json: dict) -> dict:
    game_name = json.get("game")
    game_page = json.get("page")

    game_folder = current_app.config.get("GAMES_FOLDER_LIVE")
    if not game_folder:
        return {"status": "error", "message": "No live data folder"}

    game_folder = game_folder / game_name

    if not game_folder.exists():
        return {"status": "error", "message": "Tuhle hru nemám k editaci"}

    page_path = game_folder / f"{game_page}.html"
    if not page_path.exists():
        return {"status": "error", "message": "Tuhle stránku hry nemám k editaci"}

    with open(page_path, "r") as f:
        content = f.read()
    return {"status": "ok", "content": content}

# set_page_html - set html content of page
@socketio.on("set_page_html")
def handle_set_page_html(json: dict) -> dict:
    game_name = json.get("game")
    game_page = json.get("page")
    page_content = json.get("content")

    header = "{% extends"
    if header not in page_content:
        return {"status": "error", "message": f"Zapomněli jste přidat {header}... na začátek souboru - mrkni na příklady"}

    game_folder = current_app.config.get("GAMES_FOLDER_LIVE")
    if not game_folder:
        return {"status": "error", "message": "No live data folder"}

    game_folder = game_folder / game_name

    if not game_folder.exists():
        return {"status": "error", "message": "Game does not exist"}

    page_path = game_folder / f"{game_page}.html"
    if not page_path.exists():
        return {"status": "error", "message": "Page does not exist"}

    with open(page_path, "w") as f:
        f.write(page_content)
    return {"status": "ok"}