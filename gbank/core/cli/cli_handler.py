import abc
import json
from typing import Any

from gbank.core.argparser import ArgumentParser
from ..baseclass import (
    BaseClass
)


# noinspection PyDeprecation
class CommandLineHandler(BaseClass):

    def __init__(self, arguments: list):
        """
        data output to print.
        self.data = {
            'output': ''
        }

        self.arg_parser = ArgumentParser([
            RecordsCheck.get_SSNRecord,
            CreditCardBot.run_creditcard_bot,
            Lisener.run_lisener,
        ], description="Test")
        """
        if type(arguments) is str:
            arguments = [arguments]

        #self.data: dict = {}
        self.data = {}
        self.arg_parser = ArgumentParser(arguments)

    @classmethod
    @abc.abstractclassmethod
    def run(cls):
        """
                try:
            self.arg_parser.parse_args()
        # Now custom errors
        except BotsLimitsReachException as e:
            # grab and insert cli command in database.
            command = self.arg_parser.get_full_command()
            e.add_queue_command(command)
            self.put_out(command)

        except RecordNotFound as e:
            self.data['errors'] = str(e)
        # any damn exception.
        except Exception as e:
            self.l.exception(e)
            self.data['internal_error'] = str(e)

        output = self.arg_parser.get_program_out()
        self.put_out(output)
        :return:
        """
        raise NotImplementedError('Method is not implemented.')

    def put_out(self, output: Any):
        """
        :param output:
        :return:
        """
        self.data['output'] = output
        print(json.dumps(self.data))
        exit()
