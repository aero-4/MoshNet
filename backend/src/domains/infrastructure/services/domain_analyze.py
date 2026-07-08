import asyncio
import datetime
from typing import Any

import httpx

from domains.domain.entities import Domain, DomainInfo, DomainAnalyze
from domains.domain.interfaces.service import ServiceI
from domains.infrastructure.services.request import Client
from domains.infrastructure.services.safebrowsing import GoogleSafeBrowsing
from domains.infrastructure.services.site_parser import SiteParser
from domains.infrastructure.services.virus_total import VirusTotalService
from domains.infrastructure.services.whois import WhoDatAsService


class DomainsAnalyze:

    def __init__(self):
        self.client = Client()
        self.services: dict[str, ServiceI] = {
            "whois": WhoDatAsService(),
            "virustotal": VirusTotalService(),
            "site": SiteParser(),
            "safebrowsing": GoogleSafeBrowsing()
        }

    async def run(self, domain_data: Domain) -> DomainAnalyze:
        keys = list(self.services.keys())
        result = await asyncio.gather(*[
            service.get_info(domain_data.domain) for service in self.services.values()
        ])
        result = DomainAnalyze(**dict(zip(keys, result)))

        await self.risk_score(domain_data.domain, result)

        return result

    async def risk_score(self, domain: str, data_info: DomainAnalyze):
        data_info.risk_score = 0

        self._age(data_info)  # возраст домена
        await self._has_https(data_info, domain)  # есть ли SSL
        self._virus_total_score(data_info)

    def _virus_total_score(self, data_info: DomainAnalyze):
        data_info.risk_score += len(data_info.virustotal.bad_statuses) * 50

    async def _has_https(self, data_info: DomainAnalyze, domain: str) -> None:
        domain = domain if "https://" in domain else f"https://{domain}"
        try:
            await self.client.send_request(url=domain, return_json=False)
        except httpx.HTTPError:
            data_info.risk_score += 50

    def _age(self, data_info: DomainAnalyze) -> None:
        date = data_info.whois.created_at
        if not date:
            return

        created_at = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        date_diff = (datetime.datetime.now() - created_at).days

        if date_diff < 30:
            data_info.risk_score += 30
        elif date_diff < 60:
            data_info.risk_score += 20
        elif date_diff < 90:
            data_info.risk_score += 10
