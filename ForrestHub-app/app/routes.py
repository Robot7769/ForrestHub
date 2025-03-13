import json
from http.cookiejar import debug
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
    ignore = [".git", ".vscode", "__pycache__", "node_modules"]
    if folder.exists():
        for folder_iter in folder.iterdir():
            if folder_iter.name in ignore:
                continue
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

    # remove games starting with dot
    top_level_routes = [route for route in top_level_routes if not route["name"].startswith(".")]
    return top_level_routes


@main.route("/")
def index():
    return render_template(
        "index.html",
        title="ForrestHub",
        same_level_routes=get_selected_level_routes("."),
        is_editable=False,
        edit_mode=db.edit_mode_is_on(),
        debug=current_app.config.get("DEBUG"),
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
    db.clear_data()
    return jsonify({"status": "success"})


@main.route("/upload-data", methods=["POST"])
def upload_data():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "Nebyl vybrán žádný soubor"})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"status": "error", "message": "Nebyl vybrán žádný soubor"})

    allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]
    if not file or file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
        return jsonify(
            {
                "status": "error",
                "message": f"Nebyl vybrán soubor s povolenou příponou: {', '.join(allowed_extensions)}",
            }
        )

    print(f"Uploading file {file.filename} that will overwrite the current data")

    try:
        # Read file content as a string and parse as JSON
        content = file.stream.read().decode("utf-8")  # Decode bytes to string
        json_data = json.loads(content)  # Load JSON from string

        db.set_data(json_data)  # Assuming db.set_data expects a dictionary or JSON object

        return jsonify({"status": "success"})

    except json.JSONDecodeError as e:
        return jsonify({"status": "error", "message": f"Chyba při načítání JSON: {e}"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Nastala neočekávaná chyba: {e}"})


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

            path_to_file_page = Path(
                f'{current_app.config.get("PAGES_FOLDER")}/{folder}/{page}'
            )

            if path_to_file_live.exists():
                return send_from_directory(path_to_file_live.parent, path_to_file_live.name)
            elif path_to_file.exists():
                return send_from_directory(path_to_file.parent, path_to_file.name)
            elif path_to_file_page.exists():
                return send_from_directory(path_to_file_page.parent, path_to_file_page.name)
            return abort(404)
        else:
            path_to_file = Path(
                f'{current_app.config.get("GAMES_FOLDER")}/{folder}/{page}.html'
            )
            path_to_file_live = Path(
                f'{current_app.config.get("GAMES_FOLDER_LIVE")}/{folder}/{page}.html'
            )

            is_editable = False
            page_html = ""
            if path_to_file.exists():
                page_html = path_to_file.read_text(encoding='utf-8')
            elif path_to_file_live.exists():
                page_html = path_to_file_live.read_text(encoding='utf-8')
                is_editable = True

            title = folder.capitalize()
            if page.lower() != "index":
                title = f"{title} - {page.capitalize()}"

            return render_template(
                f"{folder}/{page}.html",
                title=title,
                folder=folder,
                page=page,
                is_editable=page_html != "",
                page_html=page_html,
                config=current_app.config,
                edit_mode=db.edit_mode_is_on(),
                host_qr_readable=current_app.config.get("HOST_QR") + ":" + str(current_app.config.get("PORT")),
                same_level_routes=get_selected_level_routes(folder),
            )

    except TemplateNotFound:
        abort(404)


@main.route("/<path:filename>")
def not_allowed(filename):
    return "Tady nic není (aplikace má pouze dvě úrovně zanoření - /folder/page)"


# Serve static files
@main.route("/assets/<path:filename>")
def static_files(filename):
    static_path = current_app.config.get("ASSETS_FOLDER")
    return send_from_directory(static_path, filename)
