
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.views import APIView
from django.http import HttpResponse

from wayneapp.services import SchemaLoader
from django.template import RequestContext, loader


class SchemaViewController(APIView):
    _schema_loader = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_loader = SchemaLoader()

    def get(self, request: Request) -> Response:
        template = loader.get_template('admin/schema_list.html')
        busines_entities = self._schema_loader.get_all_business_entity_names()

        schemas = {}

        for entity in busines_entities:
            list_versions = self._schema_loader.get_all_versions(entity)
            schemas[entity] = {}
            for entity_version in list_versions:
                schemas[entity][entity_version] = self._schema_loader.load(entity, entity_version)

        context = {}
        context['schema_list'] = schemas

        return HttpResponse(template.render(context))
