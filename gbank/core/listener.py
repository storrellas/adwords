from subprocess import Popen
from time import sleep

from .baseclass import BaseClass
from ..constant import Constant
from ..helper import get_setting


class Lisener(BaseClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _check_if_any_process_bot(self) -> int:
        bots = sum(1 for _ in self._get_bots_from_db(Constant.BOT.PROCESS))

        return get_setting('maximum_bots') <= bots

    @staticmethod
    def run_lisener():
        interval = get_setting('bot_job_interval')
        instance = Lisener()

        # schedule.every(interval).minutes.do(instance.run_check)

        while True:
            # schedule.run_pending()
            # sleep(1)
            instance.run_check()
            sleep(60 * interval)

    @classmethod
    def _run_in_bg(cls, command: str):
        if command is None:
            return

        print('Running:', command)
        return Popen(command, shell=True)

    def run_check(self):
        print('Running BotJob...')
        order_table = get_setting('order_table')

        i = 1
        # only allow maximum bots to be run.
        print('Getting list of queue bots.')
        bots = list(self._get_bots_from_db(Constant.BOT.QUEUE))
        for bot in bots:
            command = bot.get(order_table.get('command'))
            if self._check_if_any_process_bot():
                continue

            if i <= get_setting('maximum_bots'):
                self._run_in_bg(command)
                # wait fot the bot to start.
                sleep(Constant.BOT_WAIT_INTERVAL)
            else:
                break
            i += 1

        print('Done!')
