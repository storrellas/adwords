from random import choice
from time import sleep

from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as ec

from gbank.constant import Constant
from gbank.core.baseclass import BaseClass
from gbank.core.baseselenium import BaseSelenium
from gbank.core.decorator import skip, look_for_selenium
from gbank.helper import read_file, data, get_setting, env


@look_for_selenium
class Google(BaseSelenium, BaseClass):

    def __init__(self):
        super().__init__()

        self.ex_driver = WebDriverWait(
            self.get_driver(),
            Constant.MAX_EXPLICT_TIMEOUT
        )

        self.ibans = []
        self.swift = []
        self.user = []

        self.username = None
        self.password = None
        self.recovery_mail = None

    def open(self):
        url = self.HOME_PAGE_LINK
        self._driver.get(url)

    def _bypass_mail_challenge(self, recovery_mail: str):
        self.l.info('Bypassing Mail Confirmation Challenge.')

        xpath = '//*[@data-challengetype="12"]'
        self.click_by_xpath(xpath)

        # wait for element.

        user_id = 'identifierId'
        self.ex_driver.until(ec.presence_of_element_located((
            By.ID, user_id
        )))

        self.l.info('Entering Username.')
        self.send_keys_by_xpath('//*[@id="identifierId"]', recovery_mail)
        self.click_by_xpath('//*[@role="button"]')

        self.ex_driver.until(ec.url_changes(
            self._driver.current_url
        ))

        # check if url contains disable.
        url = self._driver.current_url
        if 'disabled/explanation' in url:
            self.l.info('Account Disabled.')
            self._driver.close()

            raise RuntimeError('Account Disabled.')
        elif 'deniedsigninrejected' in url:
            self.l.info('Login Not Possible.')
            self._driver.close()

            raise RuntimeError('Login Not Possible.')
        elif 'myaccount.' in url:
            self.l.info('Need to bypass this.')
            # click continue bla bla
        elif 'ad' in url:
            self.l.info('Login Successfully!')

    @skip
    def login(self, username: str, password: str, recovery_mail: str):
        self.username = username
        self.password = password
        self.recovery_mail = recovery_mail

        self.l.info('Logging..')

        self._driver.refresh()
        btn = 'identifierNext'
        self.ex_driver.until(ec.presence_of_element_located((
            By.ID, btn
        )))

        self.l.info('Entering Username.')
        self.send_keys_by_xpath('//*[@id="identifierId"]', username)
        self._driver.find_element_by_id(btn).click()

        self.l.info('Entering Password.')
        pass_name = 'password'

        self.ex_driver.until(ec.visibility_of_element_located((
            By.NAME, pass_name
        )))

        btn = "passwordNext"
        self.ex_driver.until(ec.presence_of_element_located((
            By.ID, btn
        )))

        self._driver.find_element_by_name(pass_name).send_keys(password)
        self._driver.find_element_by_id(btn).click()

        self.ex_driver.until(ec.url_changes(
            self._driver.current_url
        ))

        sleep(Constant.SELENIUM_WAIT_INTERVAL * 3)
        # look for challenge.
        url = self._driver.current_url
        if 'deniedsigninrejected' in url:
            self._driver.close()
            raise RuntimeError("Couldn't sign you in")
        elif 'signin/v2/challenge/selection' in url:
            return self._bypass_mail_challenge(recovery_mail)

    def _del_bank(self):
        xpath = '//div[contains(@name, "ok")]'
        for bank in self._driver.find_elements_by_xpath(xpath):
            if bank.is_displayed():
                bank.click()

    def delete_bank(self):
        self.l.info('Waiting for iframe..')
        # wait i frame.
        self.wait_for_i_frame()
        self.switch_to_i_frame()

        banks_delete_xpath = '//div[contains(text(), "Remove")]'

        banks = list(filter(lambda ele: ele.is_displayed(), self._driver.find_elements_by_xpath(banks_delete_xpath)))
        self.l.info('Total Banks: %s' % len(banks))
        for bank in banks:
            if bank.is_displayed() and bank.is_enabled():
                bank.click()
                sleep(Constant.SELENIUM_WAIT_INTERVAL)
                self._del_bank()

                self._driver.switch_to_default_content()
                sleep(Constant.SELENIUM_WAIT_INTERVAL)

                self.wait_for_i_frame()

                self.l.info('Remaining Banks: %d To remove.' % (len(banks) - 1))

                return (len(banks) - 1) >= 1

    def wait_for_i_frame(self):

        # wait for i frame tag
        self.ex_driver.until(ec.presence_of_element_located((
            By.TAG_NAME, 'iframe'
        )))

    def switch_to_i_frame(self):
        self.wait_for_i_frame()

        frame = self._driver.find_element_by_tag_name('iframe')

        # switch.
        self._driver.switch_to_frame(frame)

    def add_bank(self):
        self.l.info('Switching to main iframe.')
        self._driver.refresh()
        self.switch_to_i_frame()

        self.l.info('Clicking on add payments..')
        self._driver.find_elements_by_class_name('b3id-widget-link')[-1].click()

        self.l.info('Switching to main iframe.')
        self.switch_to_i_frame()

        # check for element.
        self.l.info('Clicking on add a bank account.')
        path = '//*[contains(text(), "Add a bank account")]'

        self.ex_driver.until(ec.presence_of_element_located((
            By.XPATH, path
        )))
        self.click_by_xpath(path)

        # wait for user element.
        # self.switch_to_i_frame()
        user_el = 'FIELD_ACCOUNT_HOLDER_NAME'
        self.ex_driver.until(ec.presence_of_element_located((
            By.NAME, user_el
        )))

        # user.
        self.l.info('Entering Username.')
        user = Faker().name()
        user = "Ramon Lloveras"
        user_element = self._driver.find_element_by_name(user_el)
        user_element.send_keys(user)

        # I BAN
        self.l.info('Entering IBAN.')
        iban = choice(read_file(data(get_setting('bank_account_filename'))))
        self.l.info(iban)

        iban_element = self._driver.find_element_by_name('FIELD_IBAN')
        iban_element.clear()
        sleep(Constant.SELENIUM_WAIT_INTERVAL)
        iban_element.send_keys(iban)

        # swift
        self.l.info('Entering SWIFT Code.')
        swift = choice(read_file(data(get_setting('swift_filename'))))
        self.l.info(swift)

        swift_element = self._driver.find_element_by_name('FIELD_SWIFT_BANK_IDENTIFIER_CODE')
        swift_element.send_keys(swift)

        # submit
        self.l.info('Submitting..')
        self._driver.find_element_by_id('saveAddInstrument').click()
        sleep(Constant.SELENIUM_WAIT_INTERVAL)

        # switch to default content.
        self._driver.switch_to_default_content()

        # wait for content.
        self.l.info('Switching to bank verification iframe.')
        path = 'bankAccountVerification'
        self.ex_driver.until(ec.presence_of_element_located((
            By.ID, path
        )))

        self._driver.switch_to_frame(
            self._driver.find_element_by_id(path)
        )

        self.l.info('Terms..')
        self.click_by_xpath("//*[contains(@class, 'checkbox-check-container')]")
        self.l.info('Clicking Save..')
        # click save.
        self.click_by_xpath('//*[@id="saveAddInstrument"]')

        self.ex_driver.until(ec.element_to_be_clickable((
            By.ID, 'cancelAddInstrument'
        )))
        self.l.info('Clicking Got it.')
        sleep(Constant.SELENIUM_WAIT_INTERVAL)
        self._driver.find_element_by_id('cancelAddInstrument').click()

        self.l.info('Saving Data..')

        with open(data('success.txt'), 'a') as out:
            out.writelines([
                "==============================================================\r\n",
                "User:\t%s\r\n" % user,
                "Iban:\t%s\r\n" % iban,
                "Swift:\t%s\r\n" % swift,
                "Account Email:\t%s\r\n" % self.username,
                "Account Password:\t%s\r\n" % self.password,
                "Account Recovery mail:\t%s\r\n" % self.recovery_mail,
                "==============================================================\r\n"
            ])

        self.swift.append(swift)
        self.ibans.append(iban)
        self.user.append(user)

        self.l.info('Saved!')

        sleep(Constant.SELENIUM_WAIT_INTERVAL)
        # switch back to normal content.
        self._driver.switch_to_default_content()
        self.switch_to_i_frame()

    def go_to_bank(self, url='https://ads.google.com/aw/billing/paymentmethods?'):
        self._driver.get(url)

        self.l.info('Deleting Banks.')
        while self.delete_bank():
            pass
        self.l.info('Banks Deleted.')

        self.l.info('Adding Banks..')
        for _ in range(0, int(env('MAX_BANKS_ADD'))):
            self.add_bank()
        self.l.info('Banks Added..')

        self.l.info('Closing Session...')
        self._driver.close()
