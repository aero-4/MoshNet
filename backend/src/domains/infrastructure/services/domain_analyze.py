import asyncio
from typing import Any

from domains.domain.entities import Domain
from domains.domain.interfaces.service import ServiceI
from domains.infrastructure.services.site_parser import SiteParser
from domains.infrastructure.services.virus_total import VirusTotalService
from domains.infrastructure.services.whois import WhoDatAsService


class DomainsAnalyze:

    def __init__(self):
        self.services: dict[str, ServiceI] = {
            "whois": WhoDatAsService(),
            "virustotal": VirusTotalService(),
            "site": SiteParser(),
        }

    async def run(self, domain_data: Domain) -> dict[Any, Any]:
        keys = list(self.services.keys())
        result = await asyncio.gather(*[
            service.get_info(domain_data.domain) for service in self.services.values()
        ])
        result = dict(zip(keys, result))

        return result
