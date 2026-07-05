import asyncio

from domains.domain.entities import Domain, DomainInfo
from domains.infrastructure.services.virus_total import VirusTotalService
from domains.infrastructure.services.whois import WhoDatAsService


class DomainsAnalyze:

    def __init__(self):
        self.services: list = [
            WhoDatAsService(),
            VirusTotalService()
        ]

    async def run(self, domain_data: Domain) -> list[DomainInfo]:
        result = await asyncio.gather(*[
            service.get_info(domain_data.domain) for service in self.services
        ])

        return result
