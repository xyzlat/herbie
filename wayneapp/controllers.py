from _ast import Dict

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.utils import json
import logging
from wayneapp.services import BusinessEntityManager, SchemaLoader
from wayneapp.validations.validator import JsonSchemaValidator

class BusinessEntityController(APIView):
    _entity_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self.logger = logging.getLogger(__name__)

    def post(self, request: Request, type: str, key: str) -> Response:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # TODO Validation Part
        # TODO validate(body[object],type)
        validator = JsonSchemaValidator()
        #response_validation = validator.validate_schema(body[object], type, version)

        version = self._get_version(body)
        try:
            self._entity_manager.update_or_create(
                type, key, body['payload']['version'], body['payload']
            )
        except Exception as e:
            return self.handle_exception(e)
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request: Request, type: str, key: str) -> Response:
        try:
            self._entity_manager.delete_by_key(
                type, key
            )
        except Exception as e:
            return self.handle_exception(e)
        return Response({}, status=status.HTTP_200_OK)

    def handle_exception(self, exception):
        self.logger.exception(exception)
        if type(exception) is AttributeError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SchemaEntityController(APIView):
    _schema_loader = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_loader = SchemaLoader()

    def get(self, request: Request, type: str, version: str) -> Response:
        json_data = self._schema_loader.load(type, version)

        return Response(json.loads(json_data), status=status.HTTP_200_OK)
