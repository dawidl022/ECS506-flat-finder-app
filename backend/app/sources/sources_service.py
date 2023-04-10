import abc
from app.listings.models import Source
from app.listings.service import get_available_sources

class BaseSourcesService(abc.ABC):
    @abc.abstractmethod
    def get_available_sources(self, sourceLocation : str) -> list[str]:
        pass
    
class SourcesService(BaseSourcesService):
    def get_available_sources(self, location_query: str) -> list[str]:
        return [str(s) for s in Source]