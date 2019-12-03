import pkgutil

class SchemaLoader:

    def load(self, type: str, version: str) -> str:
        file_content = pkgutil.get_data('wayne_json_schema', type + '/' + type + '_' + version + '.json')
        if file_content == None:
            json_string = '{}'
        else:
            json_string = file_content.decode('utf-8')

        return json_string
