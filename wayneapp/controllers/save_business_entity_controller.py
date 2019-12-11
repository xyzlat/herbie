from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from wayneapp.constants import ControllerConstants as Constants
from wayneapp.controllers.utils import ControllerUtils
from wayneapp.services import BusinessEntityManager, SchemaLoader, JsonSchemaValidator
from rest_framework.permissions import IsAuthenticated


class SaveBusinessEntityController(APIView):
    _entity_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self._logger = logging.getLogger(__name__)
        self._validator = JsonSchemaValidator()
        self._schema_loader = SchemaLoader()
        self._permission_classes = (IsAuthenticated,)

    def post(self, request: Request, business_entity: str) -> Response:
        if not self.user_is_authorized(business_entity, request):
            return ControllerUtils.unauthorized_response()
        if not self._validator.business_entity_exist(business_entity):
            return ControllerUtils.business_entity_not_exist_response(business_entity)

        body = ControllerUtils.extract_body(request)

        if Constants.VERSION not in body:
            return ControllerUtils.custom_response(
                Constants.VERSION_MISSING,
                status.HTTP_400_BAD_REQUEST
            )

        version = body[Constants.VERSION]
        key = body[Constants.KEY]
        payload = body[Constants.PAYLOAD]
        error_messages = self._validator.validate_schema(payload, business_entity, version)

        if error_messages:
            return ControllerUtils.custom_response(error_messages, status.HTTP_400_BAD_REQUEST)

        created = self._entity_manager.update_or_create(
            business_entity, key, version, payload
        )

        return self._create_response(created, key, version)

    def _create_response(self, created, key, version):
        if created:
            return ControllerUtils.custom_response(
                Constants.SAVE_MESSAGE.format(key, version),
                status.HTTP_201_CREATED
            )

        return ControllerUtils.custom_response(
            Constants.UPDATE_MESSAGE.format(key, version),
            status.HTTP_200_OK
        )

    def user_is_authorized(self, business_entity: str, request: Request) -> bool:
        permissions = Permission.objects.filter(user=request.user).all()
        permissions_code_names = [permission.codename for permission in permissions]
        add_permission = ControllerUtils.add_permission_string(business_entity)
        change_permission = ControllerUtils.change_permission_string(business_entity)

        return (add_permission in permissions_code_names) and (change_permission in permissions_code_names)
