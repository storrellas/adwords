class BaseConstant:
    """

    """

    PROXY_EXTENSION_URL = "chrome-extension://ggmdpepbjljkkkdaklfihhngmmgmpggp/options.html"

    # Maximum Retries limit for
    MAX_RETRIES = 50
    """
    Maximum Retries limit for class. look at 
    """

    BOT_WAIT_INTERVAL = 15
    LOG_CHROMEDRIVER = 'logs/chromedriver.log'
    WHITELIST_EXCEPTIONS = [
        'BotsLimitsReachException'
    ]

    LOG_INFO = 'logs/logs.log'
    LOG_EXCEPTION = 'logs/exception.log'

    # web driver attribute name for decorator.
    WEBDRIVER_ATTR_NAME = '_driver'

    # ENVIRONMENTAL file which contains all required stuff like Database connection etc.
    SELENIUM_WAIT_INTERVAL = 3
    ENV_PATH = ".env"

    # JSON settings file which contains information for bot.
    # Where it should not ran if memory usage is >= 15
    SETTINGS_PATH = "settings.json"

    class BOT(object):
        PROCESS = "In Process"
        ERROR = "Error"
        QUEUE = "Queue"
