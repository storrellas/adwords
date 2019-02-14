import logging

from .database import Database


# TODO there is performance issue. The file loggers are being created multiple times for same class.
# todo also files are not closing
class DBHandler(logging.Handler):

    def __init__(self, column_id: int, *args, **kwargs):
        # include helper function
        from ..helper import env

        super().__init__(*args, **kwargs)
        self._column_id = column_id

        # table name. By Default load it from database
        self._table = env('TABLE')
        # column name for storing logs
        self._column_name = env('OUTPUT')

        # generate am database
        self.db = Database()

    def emit(self, record: logging.LogRecord):
        logs: str = ''

        # get exists logs
        already_exists = self.db.get_first(self._table, {'id': self._column_id})[self._column_name]
        exists = "" if already_exists is None else already_exists
        logs += exists

        # update logs now.
        logs += self.format(record) + "\n"

        # data
        data = {
            self._column_name: logs,
            'id': self._column_id
        }

        # now store the log into database.
        table = self.db[self._table]
        table.update(data, ['id'])


class LoggerFilter(logging.Filter):

    def __init__(self, level: list or int, name=''):
        super().__init__(name)
        self.level = level

    def filter(self, record) -> bool:
        return record.levelno not in self.level if type(self.level) is list else record.levelno != self.level


class Logger(object):

    DEFAULT_FORMATTER_STRING = "%(name)-12s: %(levelname)-8s %(message)s"

    def __init__(self):
        self.handlers = []

        self.name = None

    def create_stream_handler(self):
        handler = logging.StreamHandler()
        self.handlers.append(handler)

        return self

    def create_file_handler(self, level: str = logging.INFO, formatter: logging.Formatter = None,
                            dont_level: int = None, *args, **kwargs):
        # log all info
        file_handler = logging.FileHandler(*args, **kwargs)
        file_handler.setLevel(level)

        if isinstance(formatter, logging.Formatter):
            file_handler.setFormatter(formatter)
        else:
            file_handler.setFormatter(logging.Formatter(self.DEFAULT_FORMATTER_STRING))

        if dont_level is not None:
            file_handler.addFilter(
                LoggerFilter(level=dont_level)
            )

        self.handlers.append(file_handler)

        return self

    def create_db_handler(self, column_id: int, *args, **kwargs):
        handler = DBHandler(column_id, *args, **kwargs)

        self.handlers.append(handler)

    def create_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)

        # check if already has attached loggers.
        if len(logger.handlers) >= len(self.handlers):
            return logger

        # set logging level
        logger.setLevel(logging.DEBUG)

        # add all handlers
        for handler in self.handlers:
            logger.addHandler(handler)

        return logger
