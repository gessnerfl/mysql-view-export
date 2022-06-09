from .model import *
from argparse import Namespace
from getpass import getpass


def __read_int_input(msg: str) -> int:
    val = input(msg)
    while val is None or val == "":
        val = input(msg)
    return int(val)


def __read_password_input(msg: str) -> str:
    val = getpass(msg)
    while val is None or val == "":
        val = getpass(msg)
    return val


def __read_string_input(msg: str) -> str:
    val = input(msg)
    while val is None or val == "":
        val = input(msg)
    return val


def complete_input(args: Namespace) -> Parameters:
    host = args.host if args.host is not None else __read_string_input('MySQL hostname: ')
    port = args.port if args.port is not None else __read_int_input('MySQL TCP port: ')
    user = args.user if args.user is not None else __read_string_input('MySQL user: ')
    password = args.password if args.password is not None else __read_password_input('MySQL user password: ')
    schema_for_export = args.schema if args.schema is not None else __read_string_input('MySQL Schema for View Export: ')
    output_path = args.out if args.out is not None else __read_string_input('Output file path: ')
    return Parameters(DbConnectionParameters(host, port, user, password), schema_for_export, output_path, args.filter,
                      args.exclude_algorithm, args.exclude_definer)
