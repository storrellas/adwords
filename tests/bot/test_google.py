from unittest import TestCase

from gbank.bot.google import Google


class TestGoogle(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = Google()

    def test_open(self):
        self.driver.open()
        url = self.driver.get_driver().current_url
        self.driver.login(url, 'tioclevjourma@gmail.com', '7NSQQbhmec')
