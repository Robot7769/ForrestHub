from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('templates/404.html', error_messages=e), 404


@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template('templates/500.html', error_messages=e), 500
