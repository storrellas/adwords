from amdataset import dataset
from selenium import webdriver as driver
from ..helper import get_screenshot, get_setting


class UnkownError(Exception):
    pass


class MaxRetriesLimit(Exception):

    def __init__(self, webdriver: driver = None):
        self._driver = webdriver

        self.screenshot = get_screenshot()

        self._take_screenshot()

    def _take_screenshot(self):
        if self._driver is not None:
            self._driver.save_screenshot(self.screenshot)

    def __str__(self):
        screen_shot = "" if self._driver is None else " Screenshot: %s" % self.screenshot
        return "Max Retries Limit Exceed Please Check what's going on.%s" % screen_shot


class BotsLimitsReachException(Exception):
    def __init__(self, order_id, msg, database: dataset.Database=None):
        self.order_id = order_id
        self.msg = msg
        self.db = database

    def add_queue_command(self, command: str) -> None or int:
        if self.db is None:
            return

        # add to queue.
        table = get_setting('order_table')
        data = {
            'id': self.order_id,
            table.get('command'): command,
        }

        column_id = self.db.update(table.get('name'), ['id'], data)

        return column_id

    def __str__(self):
        return self.msg
