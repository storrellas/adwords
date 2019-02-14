from gbank.bot.google import Google
from gbank.helper import data, get_setting, read_file, get_google_accounts


class GoogleMain(object):

    @staticmethod
    def main():
        accounts = get_google_accounts(
            read_file(data(get_setting("google_account_filename")))
        )

        for account in accounts:
            driver = Google()
            driver.open()
            login = driver.login(*account)

            if login is False:
                continue

            driver.go_to_bank()
