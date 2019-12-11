from django.core.management import BaseCommand
from django.core.paginator import Paginator, Page
from wayneapp.constants import CommandsConstants as Constants
from wayneapp.services import BusinessEntityManager, logging, settings, MessagePublisher


class Command(BaseCommand):

    help = 'publish all data from a business entity to the business entity channel/topic'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self._logger = logging.getLogger(__name__)
        self._chunk_size = settings.CHUNK_SIZE
        self._message_service = MessagePublisher()

    def add_arguments(self, parser):
        parser.add_argument(Constants.BUSINESS_ENTITY, type=str)

    def handle(self, *args, **kwargs):
        business_entity = kwargs[Constants.BUSINESS_ENTITY]
        queryset = self._entity_manager.find_all(business_entity)
        paginator = Paginator(queryset, self._chunk_size)
        page = paginator.get_page(Constants.FIRST_PAGE)
        self._send_entities(page)
        while page.has_next():
            next_page = page.next_page_number()
            page = paginator.get_page(next_page)
            self._send_entities(page)
        self._message_service.shutdown()

    def _send_entities(self, page: Page) -> None:
        for business_entity in page.object_list:
            self._message_service.send_entity_update_message(business_entity)
