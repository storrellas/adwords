from argparse import (
    ArgumentParser as argParse,
    Namespace
)
from subprocess import list2cmdline
from typing import (
    get_type_hints,
    Callable,
    Any)
from inspect import (
    signature,
    Parameter
)
from sys import argv


class ArgumentParser(argParse):

    def __init__(self, func: list, *args, **kwargs):
        #self._out: Any = None
        self._out = None

        self.funcs = func

        super().__init__(conflict_handler="resolve", *args, **kwargs)

        for func in self.funcs:
            self._add_program_command(func)

    @classmethod
    def _get_func_params(cls, func: Callable) -> dict:
        params = get_type_hints(func)

        if 'return' in params:
            del params['return']

        return params

    def _add_program_command(self, func: Callable) -> None:
        params = self._get_func_params(func)
        # replace function _ with -
        name = func.__name__.replace('_', '-')

        # set head group
        self.add_argument('-' + name, action='store_true')

        # add required arguments
        required_arguments = self.add_argument_group("Required Arguments Of {}".format(name))
        # optional arguments
        optional_arguments = self.add_argument_group("Optional Arguments Of {}".format(name))

        # get params
        for param in params:
            type_hint = params.get(param)
            default = signature(func).parameters.get(param).default
            if default == Parameter.empty:
                # TODO take a look at this and think about it how you wanna resolve.
                # https://stackoverflow.com/questions/15753701/argparse-option-for-passing-a-list-as-option
                if type_hint is list or type_hint is iter:
                    required_arguments.add_argument("--" + param, nargs="+", required='-' + name in argv)
                    continue
                required_arguments.add_argument("--" + param, type=type_hint, required='-' + name in argv)
            else:
                if type_hint is list or type_hint is iter:
                    optional_arguments.add_argument("--" + param, nargs="*", required='-' + name in argv)
                    continue
                optional_arguments.add_argument("--" + param, type=type_hint, default=default)

    def _run_program(self, fun: Callable, args: Namespace) -> None:
        params = self._get_func_params(fun)

        kwargs = {}

        for param in params:
            default = signature(fun).parameters.get(param).default
            if default != Parameter.empty:
                kwargs[param] = default
            kwargs[param] = getattr(args, param)

        self._out = fun(**kwargs)

    def get_program_out(self) -> Any:
        return self._out

    def parse_args(self, *args, **kwargs) -> Namespace:
        args = super().parse_args(*args, **kwargs)

        for fun in self.funcs:
            if getattr(args, fun.__name__):
                self._run_program(fun, args)
                return args

        return args

    @classmethod
    def get_full_command(cls, cli: bool = True) -> list or list:
        return list2cmdline(argv) if cli else argv
