from random import choice
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_helper import Helper

from ..constant import Constant


class BaseSelenium(Helper):

    def __init__(self, *args, **kwargs):
        from ..helper import env, root

        # Disable GPU To reduce a bit performance.
        # Enable Headless mode.

        # look for authentication ip
        auth_proxy = None

        # Options
        options = Options()
        options.add_argument("--disable-gpu")

        # set sand box
        options.add_argument("--no-sandbox")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--no-default-browser-check")
        options.add_argument('--disable-infobars')

        # look for data like proxies etc.
        use_proxies_from_db = env('USE_PROXIES_FROM_DB').lower() == 'true'
        if env('USE_PROXY').lower() == 'true' and not use_proxies_from_db:
            options.add_argument("--proxy-server=%s" % env('PROXY_IP'))
        elif use_proxies_from_db:
            from ..helper import data

            proxy = self.db.get_proxy()

            # TODO: get rid of this conflict shit. Cannot use Baselcass in this class.
            self.l.info('Using Proxy from database. Proxy: ' + proxy)

            # check if proxy has authentication required.
            if len(proxy.split(':')) >= 3:
                options.add_extension(data("crx", "Proxy Auto Auth.crx"))
                auth_proxy = True
                ip = "{}:{}".format(proxy.split(':')[0], proxy.split(':')[1])

                self.l.info('Proxy: %s' % ip)
                options.add_argument("--proxy-server=%s" % ip)
            else:
                options.add_argument("--proxy-server=%s" % proxy)

        elif env('USE_PROXIES_FROM_FILE').lower() == 'true':
            self.l.info('Using Proxy from File.')

            from ..helper import get_setting, data

            proxy = self.get_proxy_from_file(
                data(get_setting('proxy_filename'))
            )

            # check if proxy has authentication required.
            if len(proxy.split(':')) >= 3:
                options.add_extension(data("crx", "Proxy Auto Auth.crx"))
                auth_proxy = True
                ip = "{}:{}".format(proxy.split(':')[0], proxy.split(':')[1])

                self.l.info('Proxy: %s' % ip)
                options.add_argument("--proxy-server=%s" % ip)
            else:
                options.add_argument("--proxy-server=%s" % proxy)

        # headless option grab from env
        if env('USE_HEADLESS').lower() == 'true':
            options.add_argument("--headless")
            options.add_argument("window-size=1280,1696")
            options.add_argument('--start-fullscreen')

        # chrome driver path
        chrome_driver_path = env('CHROMEDRIVER_PATH')

        # run chrome.
        self._driver = webdriver.Chrome(executable_path=chrome_driver_path,
                                        options=options,
                                        service_args=['--verbose', '--log-path=%s' % root(Constant.LOG_CHROMEDRIVER)],
                                        *args, **kwargs)

        # look for auth proxy.
        if auth_proxy:
            sleep(Constant.SELENIUM_WAIT_INTERVAL)

            self.l.info('Authenticating proxy.')

            # check chrome windows.
            windows = self._driver.window_handles

            if len(windows) >= 2:
                self._driver.switch_to_window(windows[-1])
                self._driver.close()
                self._driver.switch_to_window(self._driver.window_handles[-1])

            self.l.info('Opening proxy extension url.')
            self._driver.get(Constant.PROXY_EXTENSION_URL)

            user = proxy.split(":")[-2]
            password = proxy.split(":")[-1]

            self.l.info('Entering Username: %s' % user)
            self._driver.find_element_by_id("login").send_keys(user)
            self.l.info('Entering Password: %s' % password)

            self._driver.find_element_by_id("password").send_keys(password)
            self._driver.find_element_by_id("retry").clear()
            self._driver.find_element_by_id("retry").send_keys("2")

            self.l.info('Clicking save.')
            self._driver.find_element_by_id("save").click()
            # wait for few seconds.
            sleep(Constant.SELENIUM_WAIT_INTERVAL)

            self.l.info('Done!')

    @staticmethod
    def get_proxy_from_file(file: str):
        """
        This will use proxies if other proxy arguments are set to false and only `use_proxies_from_file` is set to True.
        :param file:
        :return:
        """
        with open(file, 'r') as fp:
            proxies = list(filter(lambda f: f.strip(), fp.read().splitlines()))
        return choice(proxies)

    def get_driver(self) -> webdriver:
        """
        Returns web driver instance.
        :return: webdriver
        """
        return self._driver

    def wait_for_ready(self):
        """
        Added For Explict waits.
        :return:
        """
        page_state = self._driver.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self._driver.execute_script('return document.readyState;')
