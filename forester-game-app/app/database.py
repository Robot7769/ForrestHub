import json
import os

from werkzeug.datastructures import FileStorage


class DatabaseException(Exception):
    pass


class Database:
    def __init__(self):
        self.directory = None
        self.file = None
        self.path_to_data = None
        self.data = {}

    def init(self, directory: str, file_name: str, clear_data: bool = False):
        if not directory or not os.path.exists(directory):
            raise DatabaseException('Path is not provided or does not exist - Database.init()')
        if not file_name or not file_name.endswith('.json'):
            raise DatabaseException('File name is not provided or is not a JSON file - Database.init()')

        self.directory = directory
        self.file = file_name
        self.path_to_data = os.path.join(directory, file_name)
        if clear_data or not os.path.exists(self.path_to_data):
            self._write_data({})
        self.data = self._read_data()

    def get_directory(self):
        return self.directory

    def get_file(self):
        return self.file

    def _write_data(self, data):
        with open(self.path_to_data, 'w') as f:
            json.dump(data, f)

    def _read_data(self):
        with open(self.path_to_data, 'r') as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = {}
        return data

    def overwrite_data_file(self, file: FileStorage):
        file.save(self.path_to_data)
        self.data = self._read_data()

    def overwrite_data_dict(self, new_data: dict):
        self._write_data(new_data)
        self.data = new_data

    def get_data(self):
        return self.data

    def get_data_key(self, key, default=None):
        return self.data.get(key, default)

    def set_data_key(self, key, value):
        self.data[key] = value
        self._write_data(self.data)

    def edit_data_key(self, key, value) -> bool:
        if key not in self.data:
            return False
        self.data[key] = value
        self._write_data(self.data)
        return True

    def delete_data_key(self, key):
        """Delete a key from the database.
        :param key: The key to delete
        :return: True if the key was deleted, False if the key was not found
        """
        if key in self.data:
            del self.data[key]
            self._write_data(self.data)
            return True
        return False
