import json
import os

from werkzeug.datastructures import FileStorage


class Database:
    def __init__(self, path: str, file_name: str):
        self.pathToData = os.path.join(path, file_name)
        if not os.path.exists(self.pathToData):
            self._write_data({})

    def _write_data(self, data):
        with open(self.pathToData, 'w') as f:
            json.dump(data, f)

    def read_data(self):
        with open(self.pathToData, 'r') as f:
            try :
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = {}
        return data

    def write_data(self, new_data):
        self._write_data(new_data)

    def save_file(self, file: FileStorage):
        file.save(self.pathToData)
        return self.read_data()
