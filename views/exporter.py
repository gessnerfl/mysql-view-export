from mysql.connector import connect, connection
from parameters.model import Parameters
from .formatter import Formatter
from .model import *
from typing import TypeVar, List, Union

T = TypeVar('T')


def distinct(views: List[T]) -> List[T]:
    result = []
    [result.append(v) for v in views if v not in result]
    return result


class ViewExporter:
    def __init__(self, params: Parameters, con: connection.MySQLConnection):
        self.__params = params
        self.__connection = con
        self.__formatter = Formatter(params)

    def provide(self) -> List[View]:
        views = self.__get_views_of_schema(self.__params.filter_condition)
        dependent_views = self.__get_dependent_views([v.name for v in views]) if self.__params.recursive else []
        all_views = distinct(views + dependent_views)
        return [self.__extend_view_metadata_with_create_statement(v) for v in all_views]

    def __get_dependent_views(self, depending_views: List[str]) -> List[ViewMetaData]:
        views_grouped = [self.__get_views_of_schema('view_definition like \'%{}%\''.format(v)) for v in depending_views]
        if len(views_grouped) > 0:
            views_flattened = [v for views in views_grouped for v in views]
            distinct_views = distinct(views_flattened)
            dependent_views = self.__get_dependent_views([v.name for v in
                                                          filter(lambda x: x.name not in depending_views,
                                                                 distinct_views)]) if self.__params.recursive else []
            return distinct(distinct_views + dependent_views)
        return []

    def __get_views_of_schema(self, filter_condition: Union[str, None]) -> List[ViewMetaData]:
        with self.__connection.cursor() as cursor:
            additional_where = " AND " + filter_condition if filter_condition is not None else ""
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
            formatted_create_statement = self.__formatter.format(result[1])
            full_create_statement = "DROP VIEW IF EXISTS {};\n{};".format(meta.name, formatted_create_statement)
            return View(meta, full_create_statement)


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
