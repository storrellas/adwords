from abc import ABC

from ..constant import Constant
from ..core.exception import MaxRetriesLimit
from ..helper import log, get_setting


# noinspection PyCallByClass
class BaseClass(ABC):

    db = None

    # bot method for getting list of currently running|completed|queue bot.
    @classmethod
    def _get_bots_from_db(cls, status: str = Constant.BOT.QUEUE):
        orders_table = get_setting('order_table')
        data = {
            orders_table.get('bot_status'): status
        }
        table = cls.db[orders_table.get('name')]
        bots = table.find(**data)

        return bots

    @classmethod
    def _update_bot_status(cls, _id: int, status: str) -> int:
        # add to queue.
        table = get_setting('order_table')
        data = {
            table.get('status'): status,
            'id': _id,
            table.get('bot_status'): status,
        }

        tbl = cls.db[table.get('name')]

        return tbl.update(data, ['id'])

    def _get_bot(self, _id: int):
        orders_table = get_setting('order_table')
        data = {
            'id': _id
        }
        table = self.db[orders_table.get('name')]

        return table.find_one(**data)

    # for checking how many times does program has retries for logic that wasn't succeed.
    _retries = 1

    # Column id for Db logging.
    _column_id = None

    # raise max retries error.
    # also accepts arguments
    @classmethod
    def _retries_limit_exceed(cls, **kwargs):
        if cls._retries >= Constant.MAX_RETRIES:
            raise MaxRetriesLimit(**kwargs)

    # for increments in retries.
    @classmethod
    def _increase_retries(cls):
        cls._retries += 1

    @classmethod
    def _get_retries(cls):
        return cls._retries

    @classmethod
    def _reset_retries(cls):
        cls._retries = 1

    # log method
    @classmethod
    def log(cls):
        return log(cls.__name__, cls._column_id)

    @classmethod
    def _set_log_column_id(cls, column_id: int):
        cls._column_id = column_id

    def __getattr__(self, name):
        if name == "l":
            return self.log()
        elif name.isupper():
            const_cls = getattr(Constant, self.__class__.__name__.upper())
            return getattr(const_cls, name)
        else:
            object.__getattribute__(object, name)
