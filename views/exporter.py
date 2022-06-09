from mysql.connector import connect, connection
from parameters.model import Parameters
from .formatter import Formatter
from .model import *
from typing import List


class ViewExporter:
    def __init__(self, params: Parameters, con: connection.MySQLConnection):
        self.__params = params
        self.__connection = con
        self.__formatter = Formatter(params)

    def provide(self) -> List[View]:
        views = self.__get_views_of_schema()
        return [self.__extend_view_metadata_with_create_statement(v) for v in views]

    def __get_views_of_schema(self) -> List[ViewMetaData]:
        with self.__connection.cursor() as cursor:
            additional_where = " AND " + self.__params.filter_condition if self.__params.filter_condition is not None else ""
            query = """
            SELECT TABLE_SCHEMA,
                   TABLE_NAME, 
                   VIEW_DEFINITION, 
                   CHECK_OPTION, 
                   IS_UPDATABLE, 
                   `DEFINER`, 
                   SECURITY_TYPE, 
                   CHARACTER_SET_CLIENT, 
                   COLLATION_CONNECTION 
            FROM information_schema.VIEWS
            WHERE TABLE_SCHEMA = '{}'{};
            """
            cursor.execute(query.format(self.__params.schema_for_export, additional_where))
            result = cursor.fetchall()
            return [ViewMetaData(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]) for i in result]

    def __extend_view_metadata_with_create_statement(self, meta: ViewMetaData) -> View:
        with self.__connection.cursor() as cursor:
            query = "SHOW CREATE VIEW {}.{}".format(meta.schema, meta.name)
            cursor.execute(query.format(self.__params.schema_for_export))
            result = cursor.fetchone()
            return View(meta, self.__formatter.format(result[1]))


class ViewExporterFactory:
    def __init__(self, params: Parameters):
        self.params = params

    def __enter__(self) -> ViewExporter:
        self.__connection = connect(host=self.params.mysql.host, port=self.params.mysql.port,
                                    user=self.params.mysql.username, password=self.params.mysql.password,
                                    database="information_schema")
        return ViewExporter(self.params, self.__connection)

    def __exit__(self, t, value, tb):
        self.__connection.close()


def factory(params: Parameters) -> ViewExporterFactory:
    return ViewExporterFactory(params)
