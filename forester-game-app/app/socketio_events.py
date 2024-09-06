from flask import Blueprint
from flask_socketio import emit

from app.init import socketio, db

socketio_bp = Blueprint('socketio', __name__)
connected_clients = 0
connected_admins = 0

game_status = 'running'


@socketio.on('send_admin_message')
def handle_admin_message(message):
    emit('admin_messages', message, broadcast=True)


@socketio.on('connect')
def handle_connect():
    global connected_clients
    connected_clients += 1
    emit('update_clients', {'count': connected_clients}, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    global connected_clients
    connected_clients -= 1
    emit('update_clients', {'count': connected_clients}, broadcast=True)

@socketio.on('get_game_status')
def handle_game_status():
    global game_status
    emit('game_status', game_status)


@socketio.on('set_game_status')
def handle_set_game_status(status: str):
    global game_status
    game_status = status
    emit('game_status', game_status, broadcast=True)


@socketio.on('get_all_db')
def handle_get_all_data(data) -> dict:
    return {'status': 'ok', 'data': db.get_data()}

@socketio.on('delete_all_db')
def handle_delete_all_data(data) -> dict:
    db.overwrite_data_dict({})
    return {'status': 'ok'}

@socketio.on('set_key')
def handle_set_key(json: dict):
    key = json.get('key')
    value = json.get('value')
    db.set_data_key(key, value)
    return {'status': 'ok'}


@socketio.on('set_key_broadcast')
def handle_set_key_broadcast(json: dict):
    key = json.get('key')
    value = json.get('value')
    db.set_data_key(key, value)
    emit(key, value, broadcast=True)
    return {'status': 'ok'}


@socketio.on('exists_key')
def handle_exists_key(key: str) -> dict:
    return {'status': 'ok', 'exists': db.get_data_key(key) is not None}


@socketio.on('get_key')
def handle_get_key(key: str, default=None) -> dict:
    return {'status': 'ok', 'data': db.get_data_key(key, default)}


@socketio.on('delete_key')
def handle_delete_key(key: str) -> dict:
    db.delete_data_key(key)
    return {'status': 'ok'}
