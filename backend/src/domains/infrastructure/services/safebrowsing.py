from core.settings import settings
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
    ) -> dict:
        if not api_key:
            return {
                "available": False,
                "matches": [],
                "error": "GOOGLE_SAFE_BROWSING_API_KEY is not configured",
            }

        payload = {
            "client": {
                "clientId": "netmoshen",
                "clientVersion": "1.0",
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION",
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": domain},
                ],
            },
        }

        data = await self.client.send_request(
            "POST",
            url=self.BASE_URL,
            json=payload,
            params={"key": api_key},
        )

        matches = data.get("matches", [])
        return {
            "available": True,
            "safe": not matches,
            "matches": matches,
        }
