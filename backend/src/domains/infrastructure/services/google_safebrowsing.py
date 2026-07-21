from core.settings import settings
from domains.domain.entities import GoogleSafeBrowsingInfo
from domains.domain.interfaces.service import ServiceI
from domains.infrastructure.services.request import Client


class GoogleSafeBrowsing(ServiceI):
    BASE_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

    def __init__(self, client: Client | None = None):
        self.client = client or Client()

    async def get_info(
        self,
        domain: str,
        api_key: str | None = settings.GOOGLE_SAFE_BROWSING_API_KEY,
    ) -> GoogleSafeBrowsingInfo | None:
        if not api_key:
            return GoogleSafeBrowsingInfo(available=False)

        checked_url = self._normalize_url(domain)
        payload = {
            "client": {
                "clientId": "netmoshen",
                "clientVersion": "1.0",
            },
            "threatInfo": {
                "threatTypes": [
                    "THREAT_TYPE_UNSPECIFIED",
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION",
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["THREAT_ENTRY_TYPE_UNSPECIFIED"],
                "threatEntries": [
                    {"url": checked_url},
                ],
            },
        }

        try:
            data = await self.client.send_request(
                "POST",
                url=self.BASE_URL,
                json=payload,
                params={"key": api_key},
            )
        except:
            return GoogleSafeBrowsingInfo(available=False)

        matches = data.get("matches", [])
        return GoogleSafeBrowsingInfo(
            available=True,
            safe=not matches,
            matches=matches,
        )

    def _normalize_url(self, domain: str) -> str:
        value = domain.strip()
        if not value.startswith(("http://", "https://")):
            value = f"https://{value}"

        return value
