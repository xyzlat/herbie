from django.core.management.base import BaseCommand

from herbieapp.services import BusinessEntityUtils, SchemaPackage

model_filename = "herbieapp/models/generated_models.py"


class Command(BaseCommand):
    help = 'Generates model classes based on the JSON schema definitions'

    def handle(self, *args, **kwargs):
        entity_names = SchemaPackage().get_all_schema_names()
        entity_names_camel_case = set(map(BusinessEntityUtils.snake_to_camel, entity_names))

        w = open(model_filename, "w")
        w.write('# generated file, should not be modified manually!\n')
        w.write('from herbieapp.models import AbstractBusinessEntity\n')

        for entity_name in sorted(entity_names_camel_case):
            w.write('\n\nclass {}(AbstractBusinessEntity):\n    pass\n'.format(entity_name))

        w.close()
        self.stdout.write("Generated classes: {}".format(entity_names_camel_case))


