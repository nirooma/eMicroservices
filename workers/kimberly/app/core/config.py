import json
import typing


class ConfigManager:
    __CONFIGURATION_FILE_NAME__ = "app/base_config.json"

    def __init__(self):
        self._file = open(self.__CONFIGURATION_FILE_NAME__)
        self._data = None

    @property
    def data(self):
        if self._data is None:
            try:
                self._data = json.load(self._file)
            except FileNotFoundError as e:
                raise FileNotFoundError("Sorry")
        return self._data

    def get(self, key: str, default_value=None):
        try:
            return self.data[key]
        except:
            return default_value

    def set(self, key: str, value: typing.Any = None):
        self._data[key] = value
        out_file = open(self.__CONFIGURATION_FILE_NAME__, "w")
        return json.dump(self.data, out_file, indent=2)

