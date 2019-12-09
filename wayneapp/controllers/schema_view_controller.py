import json
from rest_framework.request import Request
from rest_framework.response import Response

from django.utils.safestring import mark_safe

from rest_framework.views import APIView
from django.http import HttpResponse

from wayneapp.services import SchemaLoader
from django.template import RequestContext, loader


class SchemaViewController(APIView):
    _schema_loader = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_loader = SchemaLoader()

    def get(self, request: Request, business_entity: str, version: str) -> Response:
        if business_entity is '':
            template = loader.get_template('admin/schema_list.html')
            context = self._get_schema_list()
        else:
            template = loader.get_template('admin/schema_details.html')
            context = self._get_schema_details(business_entity, version)

        return HttpResponse(template.render(context))

    def _get_schema_list(self):
        busines_entities = self._schema_loader.get_all_business_entity_names()
        schemas = {}

        for entity in busines_entities:
            list_versions = self._schema_loader.get_all_versions(entity)
            schemas[entity] = list_versions

        context = {'schema_list': schemas}

        return context

    def _get_schema_details(self, business_entity: str, version: str) -> Response:

        json_data = self._schema_loader.load(business_entity, version)
        context = {
            'schema_json': mark_safe('<pre id="json-renderer" class="json-document">' + json_data + '</pre>'),
            'business_entity': business_entity,
            'version': version
        }

        return context
