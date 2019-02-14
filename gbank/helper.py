from os.path import (
    abspath,
    dirname,
    join
)
from os import (
    sep,
    environ
)
from logging import (
    ERROR
)
from shutil import rmtree
from time import strftime
from typing import Any

from dotenv import load_dotenv
from random import randint
from json import load
from psutil import virtual_memory

from .constant import Constant
from .core.logger import Logger
from .core.baseselenium import BaseSelenium


class DictToObj(object):
    """
    This will convert dict to object attribute.
    """

    def __init__(self, obj: dict, dont_convert_all=False):
        self.obj = obj
        for n, v in obj.items():
            if isinstance(v, dict) and not dont_convert_all:
                setattr(self, n, DictToObj(v))
            else:
                setattr(self, n, v)

    def __str__(self):
        attrs = ", ".join(self.obj.keys())
        _str = "<%s contains attributes of [%s]>" % (self.__class__.__name__, attrs)
        return _str

    def __repr__(self):
        return self.__str__()


# noinspection PyBroadException
def root(*uri, full_root: bool=True) -> str:
    """
    Returns root repository path of project.
    For example we have project name as `test`
    there we have `docs` and `tests` folder and another `test1`.
    Where `test1` is repository path and `test` is full root path.

    :param uri: any uri for joining with path. e.g we give test then it will return `path/test`.
    :param full_root: True for full Project path.
    :return: string
    """
    _dir = dirname(abspath(__file__)).split(sep)
    if full_root:
        del _dir[-1:]

    return abspath(join(sep.join(_dir), *uri))


def env(env_name: str) -> str:
    """
    It will return value of anything define in .env file
    :param env_name:
    :return:
    """
    # load config file into path
    load_dotenv(dotenv_path=root(Constant.ENV_PATH))

    return environ.get(env_name)


def data(*uri, **kwargs) -> Any:
    """
    This will return full path of data. Which is actually used to store raw data
    Our project have another directory `data` it will return path of it.
    And anything else with path to return given to it. Like we give another param as `database`.
    It will return `full_absolute_path/data/database`.

    :param uri: uri path to include same as for root.
    :param kwargs: full_root param for `root` function.
    :return: string
    """
    return root('data', *uri, **kwargs)


def log(name: str, column_id: int = None) -> Logger:
    """

    :param name: logger name.
    :param column_id: column id of database for storing logs to.
    :return: Logger
    """
    logger = Logger()
    logger.create_file_handler(filename=root(Constant.LOG_EXCEPTION), level=ERROR)
    logger.create_file_handler(filename=root(Constant.LOG_INFO), dont_level=ERROR)
    if env('ENABLE_STREAM_LOGGING').lower() == 'true':
        logger.create_stream_handler()

    # add database handler if column id isn't null.
    if column_id is not None:
        logger.create_db_handler(column_id)

    return logger.create_logger(name)


def get_memory_usage() -> float:
    """
    This will return total percentage of memory being used.

    :return: float
    """

    return virtual_memory().percent


def randomize_number(string: str, delimeter: str, starting_range: int = 0, ending_range: int = 9) -> str:
    """
    This will randomized any string with given pattern. For example we have `569xxx` and where `x` is going to
    be replaced with any random number.
    :param string: any string
    :param delimeter: Like we give `x` in `12xxx` then it will replace `x`.
    :param starting_range: The minimum number for randomizing.
    :param ending_range: The  maximum number for randomizing.
    :return: string
    """
    numbers = map(
        lambda x: x.replace(delimeter,  str(randint(starting_range, ending_range))), string
    )
    numbers = list(numbers)

    return ''.join(numbers)


def get_setting(name: str = None, file: str = Constant.SETTINGS_PATH) -> Any or None:
    """
    This will read `settings.json` then it will return value of name.
    :param name: value name.
    :param file: path to json.
    :return: DictToObj
    """
    with open(root(file), 'rb') as j:
        json = load(j)

    json = DictToObj(json)

    if name is not None:
        return getattr(json, name, None)
    else:
        return json


def check_selenium_element_exists(func: callable, exception: callable, *args, **kwargs) -> bool or callable:
    try:
        return func(*args, **kwargs)
    except exception:
        return False


def get_screenshot(delimeter: str = "screenshot_", screen_shot_path: str = None) -> str:
    file = delimeter + strftime("%Y%m%d-%H%M%S") + ".png"
    path = root("logs/screenshots/" + file) if screen_shot_path is None else join(screen_shot_path, file)

    return path


def take_screenshot(bot: BaseSelenium, section_name: str = None, store_into_web: bool = False) -> str:
    ss_path = env('SCREENSHOT_WEB_PATH') if store_into_web else None
    if section_name is not None:
        path = get_screenshot(section_name, ss_path)
    else:
        path = get_screenshot(screen_shot_path=ss_path)
    bot.get_driver().save_screenshot(path)

    return path


def read_file(file: str):
    with open(file, 'r') as out:
        lines = out.read().splitlines()

    return lines


def get_google_accounts(lines: list):
    return list(map(lambda x: tuple(x.split('\t')), lines))


# def self_destruct(path: root()):
#     rmtree()
