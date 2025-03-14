import os
import pathlib
from pathlib import Path

from flask import current_app
from jinja2 import FileSystemLoader, TemplateNotFound


class CustomLoader(FileSystemLoader):
    def get_source(self, environment, template):
        if template.startswith("templates/"):
            template_path = pathlib.Path(current_app.config["TEMPLATES_FOLDER"]) / template[10:]
        elif Path(current_app.config["GAMES_FOLDER_LIVE"]/template).exists():
            template_path = pathlib.Path(current_app.config["GAMES_FOLDER_LIVE"]) / template
        elif Path(current_app.config["GAMES_FOLDER"]/template).exists():
            template_path = pathlib.Path(current_app.config["GAMES_FOLDER"]) / template
        elif Path(current_app.config["PAGES_FOLDER"]/template).exists():
            template_path = pathlib.Path(current_app.config["PAGES_FOLDER"]) / template
        else:
            template_path = pathlib.Path(current_app.config["TEMPLATES_FOLDER"]) / "menu.html"

        if not template_path.exists():
            raise TemplateNotFound(template)

        with open(
                template_path, "r", encoding="utf-8"
        ) as f:
            source = f.read()
        mtime = os.path.getmtime(template_path)
        return source, template_path, lambda: mtime == os.path.getmtime(template_path)