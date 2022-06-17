from typing import Union


class InvalidConfigurationException(Exception):
    def __init__(self, message):
        self.message = message


def check_param(name: str, value: str):
    if not value or value.isspace():
        raise InvalidConfigurationException(
            "Required connection parameter {} is missing".format(name))


def check_port(name: str, value: int):
    if value <= 0:
        raise InvalidConfigurationException(
            "Required connection parameter port is not valid or missing".format(name))


class DbConnectionParameters:
    def __init__(self, host: str, port: int, username: str, password: str):
        check_param("host", host)
        check_port("port", port)
        check_param("username", username)
        check_param("password", password)
        self.host = host
        self.port = port
        self.username = username
        self.password = password


class Parameters:
    def __init__(self, mysql: DbConnectionParameters, schema_for_export: str, output_file: str,
                 filter_condition: Union[str, None], exclude_algorithm: bool, exclude_definer: bool,
                 recursive: bool):
        self.mysql = mysql
        self.schema_for_export = schema_for_export
        self.output_file = output_file
        self.filter_condition = filter_condition
        self.exclude_algorithm = exclude_algorithm
        self.exclude_definer = exclude_definer
        self.recursive = recursive
