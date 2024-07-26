from flask import Blueprint
from flask_socketio import emit

from app.init import socketio, db

socketio_bp = Blueprint('socketio', __name__)
connected_clients = 0
connected_admins = 0


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


@socketio.on('connect_admin')
def handle_connect_admin():
    global connected_admins
    connected_admins += 1
    emit('update_admins', {'count': connected_admins}, broadcast=True)


@socketio.on('disconnect_admin')
def handle_disconnect_admin():
    global connected_admins
    connected_admins -= 1
    emit('update_admins', {'count': connected_admins}, broadcast=True)


@socketio.on('set')
def handle_set(json):
    key = json.get('key')
    value = json.get('value')
    db.set_data_key(key, value)
    return {'status': 'success'}


@socketio.on('get')
def handle_get(key):
    return {'value': db.get_data_key(key)}


@socketio.on('edit_data')
def handle_edit_data(json):
    key = json.get('key')
    value = json.get('value')
    if db.edit_data_key(key, value):
        return {'status': 'success'}
    return {'status': 'error', 'message': 'Key not found'}


@socketio.on('delete_data')
def handle_delete_data(key):
    if db.delete_data_key(key):
        return {'status': 'success'}
    return {'status': 'error', 'message': 'Key not found'}
