from app.init import db
from app.utils import get_local_ip_address
from flask import Blueprint, render_template, abort, send_from_directory, current_app, jsonify, request
from jinja2 import TemplateNotFound

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('menu/index.html')


@main.route('/download-data')
def download_data():
    return send_from_directory(current_app.config['ROOT_DIR'], current_app.config['DATAFILE'], as_attachment=True)


@main.route('/clear-data')
def clear_data():
    db.overwrite_data_dict({})
    return jsonify({"status": "success"})


@main.route('/upload-data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})
    file = request.files['file']

    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})

    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    if (
            not file
            or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions
    ):
        return jsonify({"status": "error", "message": f"Invalid file type - allowed extensions: {allowed_extensions}"})
    print(f'Uploading file {file.filename} that will overwrite the current data')
    db.overwrite_data_file(file)
    return jsonify({"status": "success"})


@main.route('/<folder>/', defaults={'page': 'index'})
@main.route('/<folder>/<page>')
def render_page(folder: str, page: str):
    try:
        # if page contains a dot, it is a file extension - serve as static file
        if '.' in page:
            return send_from_directory(current_app.config.get("GAMES_FOLDER"), f'{folder}/{page}')
        return render_template(
            f'{folder}/{page}.html',
            title=f'{folder.capitalize()}',
            folder=folder,
            page=page,
            data=db.get_data(),
            ip_address=get_local_ip_address(),
            config=current_app.config,
        )

    except TemplateNotFound:
        abort(404)


# Serve static files
@main.route('/assets/<path:filename>')
def static_files(filename):
    static_path = current_app.config.get("ASSETS_FOLDER")
    return send_from_directory(static_path, filename)
