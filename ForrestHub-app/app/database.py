import json
import os
import asyncio
from nanoid import generate


class DatabaseException(Exception):
    pass


VAR = "VAR_"
ARR = "ARR_"


def save_data(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.save_to_file()
        return result
    return wrapper


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
        if clear_data:
            self.clear_data()
        self.load_data()

    def save_to_file(self):
        with open(self.path_to_data, 'w') as f:
            json.dump(self.data, f, indent=4)
    def load_data(self):
        if not os.path.exists(self.path_to_data):
            self.save_to_file()
        with open(self.path_to_data, 'r') as f:
            self.data = json.load(f)

    def clear_data(self):
        self.data = {}
        self.save_to_file()

    async def save_data_loop(self):
        await asyncio.sleep(2)
        while True:
            self.save_to_file()
            await asyncio.sleep(15)
            print('Saving data to file...')

    def get_all_data(self):
        return self.data

    ##########################################

    def db_var_get_key(self, project: str, key: str, default_value=None):
        project = VAR + project
        if project not in self.data:
            return default_value
        return self.data[project].get(key, default_value)

    @save_data
    def db_var_set_key(self, project: str, key: str, value):
        project = VAR + project
        if project not in self.data:
            self.data[project] = {}
        self.data[project][key] = value

    @save_data
    def db_var_delete_key(self, project: str, key: str):
        project = VAR + project
        if project in self.data and key in self.data[project]:
            del self.data[project][key]
            return True
        return False

    def db_var_exists_key(self, project: str, key: str):
        project = VAR + project
        return project in self.data and key in self.data[project]

    ##########################################

    # add record
    @save_data
    def array_add_record(self, project: str, array_name: str, value):
        project = ARR + project
        if project not in self.data:
            self.data[project] = {}
        if array_name not in self.data[project]:
            self.data[project][array_name] = {}
        self.data[project][array_name][generate(size=10)] = value

    # remove record
    @save_data
    def array_remove_record(self, project: str, array_name: str, record_id: str):
        project = ARR + project
        if self._record_exists(project, array_name, record_id):
            del self.data[project][array_name][record_id]
            return True
        return False

    # update record
    @save_data
    def array_update_record(self, project: str, array_name: str, record_id: str, value):
        project = ARR + project
        if self._record_exists(project, array_name, record_id):
            self.data[project][array_name][record_id] = value
            return True
        return False

    def _record_exists(self, project_prefix: str, array_name: str, record_id: str) -> bool:
        return project_prefix in self.data and array_name in self.data[project_prefix] and record_id in self.data[project_prefix][array_name]

    def array_get_record_id(self, project: str, array_name: str, record_id: str):
        project = ARR + project
        return self.data[project][array_name].get(record_id, {}) if project in self.data and array_name in self.data[project] else {}

    def array_get_all_records(self, project: str, array_name: str):
        project = ARR + project
        return self.data[project].get(array_name, {}) if project in self.data else []


    @save_data
    def array_clear_records(self, project: str, array_name: str):
        project = ARR + project
        if project in self.data and array_name in self.data[project]:
            self.data[project][array_name] = {}
            return True
        return False


    def array_list_projects(self):
        # return only keys starting with ARR_
        # return list(self.data.keys())
        return [key[4:] for key in self.data.keys() if key.startswith(ARR)]
