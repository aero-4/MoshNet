import asyncio
import datetime

import httpx

from domains.domain.entities import Domain, DomainAnalyzeInfo
from domains.domain.interfaces.service import ServiceI
from domains.infrastructure.services.google_safebrowsing import GoogleSafeBrowsing
from domains.infrastructure.services.request import Client
from domains.infrastructure.services.site_parser import SiteParser
from domains.infrastructure.services.virus_total import VirusTotalService
from domains.infrastructure.services.whois import WhoDatAsService
from domains.infrastructure.services.yandex_safebrowsing import YandexSafeBrowsing


class DomainsAnalyze:

    def __init__(self):
        self.client = Client()
        self.services: dict[str, ServiceI] = {
            "whois": WhoDatAsService(),
            "virustotal": VirusTotalService(),
            "site": SiteParser(),
            "google_safebrowsing": GoogleSafeBrowsing(),
            "yandex_safebrowsing": YandexSafeBrowsing(),
        }

    async def run(self, domain_data: Domain) -> DomainAnalyzeInfo:
        keys = list(self.services.keys())
        result = await asyncio.gather(*[
            service.get_info(domain_data.domain) for service in self.services.values()
        ])
        result = DomainAnalyzeInfo(**dict(zip(keys, result)))

        await self.risk_score(domain_data.domain, result)

        return result

    async def risk_score(self, domain: str, data_info: DomainAnalyzeInfo):
        self._age_score(data_info)
        self._virus_total_score(data_info)
        self._google_safe_browse_score(data_info)
        self._yandex_safe_browse_score(data_info)
        await self._has_https_score(data_info, domain)

    def _google_safe_browse_score(self, data_info: DomainAnalyzeInfo):
        if data_info.google_safebrowsing.available and not data_info.google_safebrowsing.safe:
            data_info.risk_score += max(len(data_info.google_safebrowsing.matches), 1) * 100

    def _yandex_safe_browse_score(self, data_info: DomainAnalyzeInfo):
        if data_info.yandex_safebrowsing.available and not data_info.yandex_safebrowsing.safe:
            data_info.risk_score += max(len(data_info.yandex_safebrowsing.matches), 1) * 100

    def _virus_total_score(self, data_info: DomainAnalyzeInfo):
        data_info.risk_score += len(data_info.virustotal.bad_statuses) * 100

    async def _has_https_score(self, data_info: DomainAnalyzeInfo, domain: str) -> None:
        domain = domain if "https://" in domain else f"https://{domain}"
        try:
            await self.client.send_request(url=domain, return_json=False)
        except httpx.HTTPError:
            data_info.risk_score += 50

    def _age_score(self, data_info: DomainAnalyzeInfo) -> None:
        date = data_info.whois.created_at
        if not date:
            return None

        created_at = self._parse_date(date)
        if not created_at:
            return None

        date_diff = (datetime.datetime.now() - created_at).days

        if date_diff < 30:
            data_info.risk_score += 30
        elif date_diff < 60:
            data_info.risk_score += 20
        elif date_diff < 90:
            data_info.risk_score += 10

    def _parse_date(self, value: str) -> datetime.datetime | None:
        normalized = value.strip()
        if normalized.endswith("Z"):
            normalized = f"{normalized[:-1]}+00:00"

        try:
            return datetime.datetime.fromisoformat(normalized).replace(tzinfo=None)
        except ValueError:
            return None
