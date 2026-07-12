import abc

from domains.infrastructure.services.request import Client


class ServiceI(abc.ABC):


    @abc.abstractmethod
    async def get_info(self, domain: str):
        pass
