from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import json
from wayneapp.constants import ControllerConstants
from wayneapp.services import SchemaLoader


class ControllerUtils:

    @staticmethod
    def unauthorized_response() -> Response:
        return ControllerUtils.custom_response(
            ControllerConstants.UNAUTHORIZED,
            status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    def business_entity_not_exist_response(business_entity: str) -> Response:
        return ControllerUtils.custom_response(
            ControllerConstants.BUSINESS_ENTITY_NOT_EXIST.format(business_entity),
            status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def custom_response(message: str, status_code: status) -> Response:
        return Response(
            {
                "message": message
            },
            status=status_code
        )
    
    @staticmethod
    def extract_body(request: Request) -> dict:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        return body

    @staticmethod
    def user_is_authorized(business_entity: str, request: Request) -> bool:
        business_entity_camel_case = SchemaLoader.snake_to_camel(business_entity)
        user = request.user
        groups = list(user.groups.all())
        groups_name = [group.name for group in groups]
        if business_entity_camel_case in groups_name:
            return True
        return False
