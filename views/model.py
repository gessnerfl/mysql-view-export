class ViewMetaData:
    def __init__(self, schema: str, name: str, definition: str, check_option: str, is_updatable: str, definer: str,
                 security_type: str, character_set_client: str, collation_connection: str):
        self.schema = schema
        self.name = name
        self.definition = definition
        self.check_option = check_option
        self.is_updatable = is_updatable
        self.definer = definer
        self.security_type = security_type
        self.character_set_client = character_set_client
        self.collation_connection = collation_connection


class View:
    def __init__(self, meta_data: ViewMetaData, create_statement: str):
        self.meta_data = meta_data
        self.create_statement = create_statement
