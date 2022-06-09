import argparse

from parameters.completion import *
from views.exporter import get_views_for_export
from views.model import View
from typing import List
import sqlparse


def write_output(views: List[View], outfile: str):
    with open(outfile, "x") as f:
        for v in views:
            f.write(sqlparse.format(v.create_statement, reindent=True, keyword_case='upper'))
            f.write("\n\n")


def run_application():
    args_parser = argparse.ArgumentParser(allow_abbrev=False, prog='mysql-view-export',
                                          description='Export database views of schema in mysql database')
    args_parser.add_argument('-H', '--host', help='the mysql hostname', type=str, required=False)
    args_parser.add_argument('-P', '--port', help='the mysql TCP port number', type=int, required=False)
    args_parser.add_argument('-S', '--schema', help='the mysql schema for which the view should be exported', type=str,
                             required=False)
    args_parser.add_argument('-u', '--user', help='the mysql username', type=str, required=False)
    args_parser.add_argument('-p', '--password', help='the mysql user password', type=str, required=False)
    args_parser.add_argument('-o', '--out', help='the file path of the output file', type=str, required=False)
    args_parser.add_argument('-f', '--filter', help='a filter condition to select only specific views', type=str,
                             required=False)
    args = args_parser.parse_args()

    params = complete_input(args)

    with get_views_for_export(params) as f:
        views = f.provide()
        write_output(views, params.output_file)


run_application()
