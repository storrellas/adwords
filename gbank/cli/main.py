from gbank.cli.google import GoogleMain
from gbank.core.cli.cli_handler import CommandLineHandler
from gbank.core.decorator import look_for_all


class CommandLine(CommandLineHandler):

    def __init__(self):
        super().__init__([
            GoogleMain.main
        ])

    def run(self):
        self.arg_parser.parse_args()

        output = self.arg_parser.get_program_out()
        self.put_out(output)


@look_for_all
def main():
    CommandLine().run()


if __name__ == '__main__':
    main()
