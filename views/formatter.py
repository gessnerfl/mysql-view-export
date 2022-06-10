from parameters.model import Parameters
import sqlparse
import re


class Formatter:

    def __init__(self, params: Parameters):
        self.params = params
        self.algorithm_regex = re.compile(r'([Aa][Ll][Gg][Oo][Rr][Ii][Tt][Hh][Mm]=)(\w+)( )?')
        self.definer_regex = re.compile(r'([Dd][Ee][Ff][Ii][Nn][Ee][Rr]=)(`?[\w\d.\-_]+`?@`?[\w\d.-_%]+`?)( )?')

    def format(self, original: str) -> str:
        stmt = self.definer_regex.sub('', original) if self.params.exclude_definer else original
        stmt = self.algorithm_regex.sub('', stmt) if self.params.exclude_algorithm else stmt

        return sqlparse.format(stmt, reindent=True, keyword_case='upper')
