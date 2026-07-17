import logging

from httpx import HTTPStatusError

from core.settings import settings
from domains.domain.entities import BadStatus, DomainInfo
from domains.domain.interfaces.service import ServiceI
from domains.infrastructure.services.request import Client


class VirusTotalService(ServiceI):
    BAD_CATEGORIES = {"malicious", "suspicious"}
    BAD_RESULTS = {
        "malicious",
        "suspicious",
        "phishing",
        "malware",
        "spam",
        "scam",
        "blacklist",
        "blacklisted",
    }

    def __init__(self, client: Client | None = None, api_key: str | None = settings.VIRUS_TOTAL_API_KEY):
        self.base_url = "https://www.virustotal.com"
        self.api_key = api_key
        self.headers = {"x-apikey": api_key, "accept": "application/json"} if api_key else {"accept": "application/json"}
        self.client = client or Client(headers=self.headers)

    async def get_info(self, domain: str) -> DomainInfo:
        if not self.api_key:
            logging.warning("VirusTotal API key is not configured")
            return DomainInfo(domain_org=domain)

        data = await self.get_domain_info(domain)
        if not data:
            return DomainInfo(domain_org=domain)

        attributes = data.get("data", {}).get("attributes", {})

        return DomainInfo(
            domain_org=domain,
            last_analysis_stats=attributes.get("last_analysis_stats"),
            bad_statuses=self.extract_bad_statuses(attributes),
        )

    async def get_domain_info(self, domain: str) -> dict | None:
        try:
            return await self.client.send_request(
                "GET",
                f"{self.base_url}/api/v3/domains/{domain}",
                headers={"x-apikey": self.api_key, "accept": "application/json"}
            )
        except HTTPStatusError as exc:
            logging.warning(
                "VirusTotal request failed: status=%s domain=%s",
                exc.response.status_code,
                domain,
            )
            return None
        except Exception:
            logging.exception("Error for request VirusTotal")
            return None

    async def scan_url(self, url: str) -> dict:
        return await self.client.send_request(
            "POST",
            f"{self.base_url}/api/v3/urls",
            headers={
                **self.headers,
                "content-type": "application/x-www-form-urlencoded",
            },
            data={"url": url},
        )

    async def analysis_info(self, id: str):
        data = await self.client.send_request("GET",
                                           f"{self.base_url}/api/v3/analyses/{id}",
                                              headers=self.headers)
        return data

    def extract_bad_statuses(self, attributes: dict) -> list[BadStatus]:
        results = attributes.get("last_analysis_results") or {}
        bad_statuses = []

        for source, result_data in results.items():
            category = result_data.get("category")
            result = result_data.get("result")
            normalized_result = str(result).lower() if result else None

            if category in self.BAD_CATEGORIES or normalized_result in self.BAD_RESULTS:
                bad_statuses.append(
                    BadStatus(
                        source=source,
                        category=category,
                        result=result,
                    )
                )

        return bad_statuses
