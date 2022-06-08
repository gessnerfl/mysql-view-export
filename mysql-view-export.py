import argparse

from parameters.completion import *


def run_application():
    args_parser = argparse.ArgumentParser(allow_abbrev=False, prog='mysql-view-export',
                                          description='Export database views of schema in mysql database')
    args_parser.add_argument('-H', '--host', help='the mysql hostname', type=str, required=False)
    args_parser.add_argument('-P', '--port', help='the mysql TCP port number', type=str, required=False)
    args_parser.add_argument('-u', '--user', help='the mysql username', type=str, required=False)
    args_parser.add_argument('-p', '--password', help='the mysql user password', type=str, required=False)
    args_parser.add_argument('-o', '--out', help='the file path of the output file', type=str, required=False)
    args = args_parser.parse_args()

    config_file = args.config
    config = complete_input(config_file)
    print(config)


run_application()
