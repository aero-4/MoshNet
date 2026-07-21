import abc


class ServiceI(abc.ABC):
    @abc.abstractmethod
    async def get_info(self, domain: str):
        pass
