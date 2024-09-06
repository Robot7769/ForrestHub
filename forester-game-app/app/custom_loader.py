import os
import pathlib
from pathlib import Path

from flask import current_app
from jinja2 import FileSystemLoader, TemplateNotFound


class CustomLoader(FileSystemLoader):
    def get_source(self, environment, template):
        if template.startswith("templates/"):
            # {% include 'templates/header.html' %}
            if current_app.config.get("LIVE_DATA_USED") and current_app.config.get("LIVE_DATA_FOLDER").exists():
                template_path = pathlib.Path(current_app.config["TEMPLATES_FOLDER_LIVE"]) / template[10:]
            else:
                template_path = pathlib.Path(current_app.config["TEMPLATES_FOLDER"]) / template[10:]
        elif current_app.config.get("LIVE_DATA_USED") and Path(current_app.config["GAMES_FOLDER_LIVE"]).exists():
            template_path = pathlib.Path(current_app.config["GAMES_FOLDER_LIVE"]) / template
        else:
            template_path = pathlib.Path(current_app.config["GAMES_FOLDER"]) / template

        if not template_path.exists():
            raise TemplateNotFound(template)

        with open(
                template_path, "r", encoding="utf-8"
        ) as f:  # Specify the encoding here
            source = f.read()
        mtime = os.path.getmtime(template_path)
        return source, template_path, lambda: mtime == os.path.getmtime(template_path)
