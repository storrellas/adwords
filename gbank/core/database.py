from amdataset import dataset
from random import choice

from sqlalchemy.pool import NullPool


class Database(dataset.Database):
    """
    Database class for connecting to database. inherited from data set.
    """
    instance = None
    """
    singleton method for avoiding multiple connections.
    """

    def __new__(cls, *args, **kwargs):
        """
        This method called before constructor so this will check and will return
        database class which is already initialized.

        :param args:
        :param kwargs:
        :return: class
        """
        if cls.instance is None:
            cls.instance = object.__new__(cls)

        return cls.instance

    def __init__(self):
        """
        Here it will check if username and password is given then it will connect
        to database otherwise. it will ignore.
        For connecting to sqlite database. It will create database inside %root%/data/dbname.

        We can leave the database empty. It will not connect to it if database driver is empty.
        """

        from ..helper import (
            env,
            data
        )

        # firstly check if we need to connect to database or not.
        connect = len(env('DATABASE_URI')) <= 1
        if connect:
            return

        """
        if username and password of database is empty then we don't have to connect to database.
        """

        driver = env('DATABASE_URI')
        if driver == 'sqlite':
            database = data('database', env('DATABASE'), full_root=True)
            url = '%s:///%s' % (driver, database)
        else:
            url = "%s://%s:%s@%s:%d/%s" % (driver, env('DATABASE_USER'), env('DATABASE_PASSWORD'),
                                           env('DATABASE_HOST'), int(env('DATABASE_PORT')), env('DATABASE'))

        # set engine commit level to read any changes from database too.
        # pool class set to `Null Pool` for sqlite because we also wanna use it in multiple
        # threads
        engine_kwargs = {
            'isolation_level': "READ UNCOMMITTED",
            'poolclass': NullPool
        }

        if not connect:
            super().__init__(url, engine_kwargs=engine_kwargs)

    def get_proxy(self) -> str:
        """
        This will grab any random proxy from database but make sure you have at least one proxy in database.
        :return: string
        """
        from ..helper import get_setting
        table = get_setting('proxies')
        data = list(self.get_all(table.get('name')))

        if len(data) <= 1:
            raise RuntimeError('Make Sure You have at least one proxy in database.')

        return choice(data).get(table.get('column'))
