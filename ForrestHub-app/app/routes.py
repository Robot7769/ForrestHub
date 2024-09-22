from pathlib import Path

from app.init import db
from app.utils import get_local_ip_address
from flask import (
    Blueprint,
    render_template,
    abort,
    send_from_directory,
    current_app,
    jsonify,
    request,
)
from jinja2 import TemplateNotFound

main = Blueprint("main", __name__)


def get_html_and_folders(folder: Path):
    res = []
    if folder.exists():
        for folder_iter in folder.iterdir():
            if folder_iter.is_dir():
                res.append(
                    {
                        "name": folder_iter.name,
                        "is_dir": True,
                    }
                )
            elif folder_iter.suffix == ".html" and folder_iter.stem != "index":
                res.append(
                    {
                        "name": folder_iter.stem,
                        "is_dir": False,
                    }
                )
    return res


def get_selected_level_routes(folder: str):
    top_level_routes = []
    folders_live = Path(current_app.config.get("GAMES_FOLDER_LIVE", "")) / folder
    if current_app.config.get("GAMES_FOLDER_LIVE") and folders_live.exists():
        top_level_routes = get_html_and_folders(folders_live)
    folders = current_app.config.get("GAMES_FOLDER", "") / folder
    if folders.exists():
        top_level_routes.extend(get_html_and_folders(folders))
    # top_level_routes.sort(key=lambda x: x.lower())
    return top_level_routes


@main.route("/")
def index():
    return render_template(
        "index.html", title="Menu", same_level_routes=get_selected_level_routes(".")
    )


@main.route("/download-data")
def download_data():
    return send_from_directory(
        current_app.config["EXECUTABLE_DIR"],
        current_app.config["DATAFILE"],
        as_attachment=True,
    )


@main.route("/clear-data")
def clear_data():
    db.overwrite_data_dict({})
    return jsonify({"status": "success"})


@main.route("/upload-data", methods=["POST"])
def upload_data():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file part"})
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"status": "error", "message": "No selected file"})

    allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]
    if not file or file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
        return jsonify(
            {
                "status": "error",
                "message": f"Invalid file type - allowed extensions: {allowed_extensions}",
            }
        )
    print(f"Uploading file {file.filename} that will overwrite the current data")
    db.overwrite_data_file(file)
    return jsonify({"status": "success"})


@main.route("/<folder>/", defaults={"page": "index"})
@main.route("/<folder>/<page>")
def render_page(folder: str, page: str):
    try:
        # if page contains a dot, it is a file extension - serve as static file
        if "." in page:
            path_to_file = Path(
                f'{current_app.config.get("GAMES_FOLDER")}/{folder}/{page}'
            )
            path_to_file_live = Path(
                f'{current_app.config.get("GAMES_FOLDER_LIVE")}/{folder}/{page}'
            )
            if path_to_file_live.exists():
                return send_from_directory(
                    path_to_file_live.parent, path_to_file_live.name
                )
            elif path_to_file.exists():
                return send_from_directory(path_to_file.parent, path_to_file.name)
            return abort(404)
        else:
            title = folder.capitalize()
            if page.lower() != "index":
                title = f"{title} - {page.capitalize()}"

            return render_template(
                f"{folder}/{page}.html",
                title=title,
                folder=folder,
                page=page,
                data=db.get_data(),
                ip_address=get_local_ip_address(),
                config=current_app.config,
                same_level_routes=get_selected_level_routes(folder),
            )

    except TemplateNotFound:
        abort(404)


@main.route("/<path:filename>")
def not_allowed(filename):
    return "Not allowed depth level 3", 404


# Serve static files
@main.route("/assets/<path:filename>")
def static_files(filename):
    static_path = current_app.config.get("ASSETS_FOLDER")
    return send_from_directory(static_path, filename)
