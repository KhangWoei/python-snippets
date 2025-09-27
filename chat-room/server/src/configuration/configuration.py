from configparser import ConfigParser
from os import path
from os import environ

_instance = None

class _Configuration:
    def __init__(self, config_path: str ="config.ini"):
        if not hasattr(self, '_initialized') :
            self._config = ConfigParser()
            self._config.read(config_path)
            self._initialized = True
    
    @property
    def address(self):
        return self._config["Server"]["Address"]

    @property
    def port(self):
        return self._config["Server"]["Port"]

def load() -> _Configuration:    
    config_path = environ.get("CHAT_SERVER_CONFIGURATION", "config.ini")

    if not path.exists(config_path):
        raise ConfigFileNotFoundExcetion(config_path)

    global _instance

    if _instance is None:
        _instance = _Configuration(config_path)

    return _instance

class ConfigFileNotFoundExcetion(Exception):
    def __init__(self, file_path: str):
        super().__init__(f"{file_path} not found")
