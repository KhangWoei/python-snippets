from sys import stderr
from logging import  getLogger, Logger, Handler, StreamHandler, FileHandler, Formatter, INFO
from platformdirs import user_log_dir
from typing import List, TypeAlias

_Level: TypeAlias = int | str

class LogInitializer():

    @staticmethod
    def init(name: str, verbosity: _Level = INFO):
        base: Logger = getLogger(name)

        if base.handlers:
            return

        base.setLevel(verbosity)

        # https://docs.python.org/3/library/logging.html#logrecord-attributes
        formatter: Formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s')

        stream_handler: Handler = StreamHandler(stderr)
        stream_handler.setFormatter(formatter)
        base.addHandler(stream_handler)
        
        try:
            log_file: str = user_log_dir(appname=name, ensure_exists=True)
            file_handler: Handler = FileHandler(log_file)
            file_handler.setFormatter(formatter)

            base.info(f"Logging to file: {log_file}")
        except (Exception) as e:
            base.error(f"Failed to setup file logging {e}. Falling back to console logger")
