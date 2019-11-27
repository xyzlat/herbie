import importlib

from wayneapp.models.models import AbstractBusinessEntity

class BusinessEntityManager:
    def get_business_entity_class(self, entity_name: str):
        models_module = importlib.import_module("wayneapp.models")

        return getattr(models_module, str(entity_name).capitalize())


    def update_or_create_business_entity(
            self,
            entity_name: str,
            key: str,
            version: int,
            data: str
    ) -> (AbstractBusinessEntity, bool):
        business_entity = self.get_business_entity_class(entity_name)
        object, created = business_entity.objects.update_or_create(
            key=key,
            version=version,
            defaults={
                'key': key,
                'version': version,
                'data': data
            }
        )

        return object


    def delete_business_entity(self, entity_name: str, key: str, version: int) -> None:
        business_entity = self.get_business_entity_class(entity_name)
        business_entity.objects.filter(key=key, version=version).delete()
