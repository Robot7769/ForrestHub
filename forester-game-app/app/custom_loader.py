import os
import sys
from flask import current_app
from jinja2 import FileSystemLoader, TemplateNotFound


def get_root_path():
    if getattr(sys, "frozen", False):
        # we are running in a bundle
        return sys._MEIPASS
    else:
        # we are running in a normal Python environment
        return current_app.config["ROOT_DIR"]


class CustomLoader(FileSystemLoader):
    def get_source(self, environment, template):
        root_path = get_root_path()
        if template.startswith("templates/"):
            template_path = os.path.join(root_path, "templates", template[10:])
        else:
            template_path = os.path.join(root_path, "pages", template)

        if not os.path.exists(template_path):
            raise TemplateNotFound(template)

        with open(
            template_path, "r", encoding="utf-8"
        ) as f:  # Specify the encoding here
            source = f.read()
        mtime = os.path.getmtime(template_path)
        return source, template_path, lambda: mtime == os.path.getmtime(template_path)
