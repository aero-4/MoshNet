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
        service_inputs = {
            "whois": domain_data.domain,
            "virustotal": domain_data.domain,
            "site": domain_data.url,
            "google_safebrowsing": domain_data.url,
            "yandex_safebrowsing": domain_data.url,
        }
        result = await asyncio.gather(*[
            service.get_info(service_inputs[key]) for key, service in self.services.items()
        ])
        result = DomainAnalyzeInfo(**dict(zip(keys, result)))

        self.risk_score(result)

        return result

    def risk_score(self, data_info: DomainAnalyzeInfo):
        self._age_score(data_info)
        self._virus_total_score(data_info)
        self._google_safe_browse_score(data_info)
        self._yandex_safe_browse_score(data_info)
        self._has_https_score(data_info)

    def _google_safe_browse_score(self, data_info: DomainAnalyzeInfo):
        if data_info.google_safebrowsing.available and not data_info.google_safebrowsing.safe:
            data_info.risk_score += max(len(data_info.google_safebrowsing.matches), 1) * 100

            for status in data_info.yandex_safebrowsing.matches:
                data_info.status.append(f"Категория проверки {status} - присвоен статус: {status}")

    def _yandex_safe_browse_score(self, data_info: DomainAnalyzeInfo):
        if data_info.yandex_safebrowsing.available and not data_info.yandex_safebrowsing.safe:
            data_info.risk_score += max(len(data_info.yandex_safebrowsing.matches), 1) * 100

            for status in data_info.yandex_safebrowsing.matches:
                data_info.status.append(f"Категория проверки {status} - присвоен статус: {status}")

    def _virus_total_score(self, data_info: DomainAnalyzeInfo):
        if data_info.virustotal and len(data_info.virustotal.bad_statuses) > 0:
            data_info.risk_score += len(data_info.virustotal.bad_statuses) * 100

            for status in data_info.virustotal.bad_statuses:
                data_info.status.append(f"Проверка от {status.source} - присвоен статус: {status.result}")

    def _has_https_score(self, data_info: DomainAnalyzeInfo) -> None:
        if not data_info.site.has_ssl:
            data_info.risk_score += 100
            data_info.status.append("Домен не подключен к SSL")

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
            data_info.status.append("Домен зарегистрирован меньше чем 1 месяца назад")
        elif date_diff < 60:
            data_info.risk_score += 20
            data_info.status.append("Домен зарегистрирован меньше чем 2 месяцев назад")
        elif date_diff < 90:
            data_info.risk_score += 10
            data_info.status.append("Домен зарегистрирован меньше чем 3 месяцев назад")

    def _parse_date(self, value: str) -> datetime.datetime | None:
        normalized = value.strip()
        if normalized.endswith("Z"):
            normalized = f"{normalized[:-1]}+00:00"

        try:
            return datetime.datetime.fromisoformat(normalized).replace(tzinfo=None)
        except ValueError:
            return None
