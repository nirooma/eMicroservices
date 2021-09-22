import json
import typing
import logging

_logger = logging.getLogger(__name__)


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
        self.data[key] = value
        out_file = open(self.__CONFIGURATION_FILE_NAME__, "w")
        _logger.info(f"{key!r} key successfully added to the base config file.")
        return json.dump(self.data, out_file, indent=2)


config = ConfigManager()