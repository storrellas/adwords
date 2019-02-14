import functools

from selenium.common.exceptions import WebDriverException

from . import exception as exceptions
from ..constant import Constant
from ..helper import take_screenshot, log, data
from .baseselenium import BaseSelenium


# TODO send notification on exception.
def mark_as_error(args: callable):
    args = list(args)
    if len(args) >= 1:
        cls = args[0]
    else:
        return
    if hasattr(cls, 'mark_as'):
        getattr(cls, 'mark_as')("3")


def unknown_exception_decorator(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log(__file__).exception(e)

            print('Some random unknown error occur', 'ignoring..')
    return wrap


def selenium_decorator(obj):
    @functools.wraps(obj)
    def wrap(*args, **kwargs):
        try:
            return obj(*args, **kwargs)
        except Exception as e:
            for arg in list(args):
                attr = Constant.WEBDRIVER_ATTR_NAME
                if hasattr(arg, attr) and isinstance(e, WebDriverException):
                    # take screen shot.
                    #driver: BaseSelenium = arg
                    driver = arg
                    path = take_screenshot(driver)
                    # add screen shot to log.
                    e.msg += " Screenshot: " + path
                    # close web driver.
                    getattr(driver, attr).quit()

                    cls = driver

                    user = getattr(cls, 'username')
                    print('Account:', user)

                    password = getattr(cls, 'password')
                    recovery_mail = getattr(cls, 'recovery_mail')
                    with open(data('error.txt'), 'a') as fp:
                        reason = 'Unknown'

                        if isinstance(e, RuntimeError):
                            reason = str(e)
                        else:
                            log(__file__).exception(e)

                        fp.writelines([
                            '%s\t%s\t%s\t%s\r\n' % (user, password, recovery_mail, reason)
                        ])

                    # raise e
            # raise e
    return wrap


def look_for_selenium(cls):
    for name, f in cls.__dict__.items():
        # needs to skip static method
        if name.startswith('__') and name.endswith('__') or not callable(f):
            continue
        setattr(cls, name, selenium_decorator(f))

    return cls


def look_for_all(func):
    return unknown_exception_decorator(func)


def skip(func: callable):
    def wrap(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('Error:', e, 'Ignoring..')

            args = list(args)

            user = args[1]
            print('Account:', user)

            password = args[2]
            recovery_mail = args[3]
            with open(data('error.txt'), 'a') as fp:
                reason = 'Unknown'

                if isinstance(e, RuntimeError):
                    reason = str(e)
                else:
                    log(__file__).exception(e)

                fp.writelines([
                    '%s\t%s\t%s\t%s\r\n' % (user, password, recovery_mail, reason)
                ])

            return False

    return wrap
