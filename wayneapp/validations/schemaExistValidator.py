# import schema load service
class SchemaExistValidator:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def schema_exist(self, schema_name: str):
        # Todo call load schema service to retrieve the list with all schemas
        schemas = [schema_name]
        if schema_name not in schemas:
            return False
        return True
