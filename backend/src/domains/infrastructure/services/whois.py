import datetime

from domains.domain.entities import DomainInfo
from domains.infrastructure.services.request import Client


class WhoDatAsService:

    def __init__(self):
        self.api = Client()
        self.base_url: str = 'https://who-dat.as93.net'

    async def get_info(self, domain: str) -> DomainInfo:
        try:
            data = await self.api.send_request(url=f"{self.base_url}/v1/whois/{domain}")
            if not data:
                return {}
        except:
            return {}


        return DomainInfo(
            domain_org=data.get("domain"),
            created_at=data.get("dates").get("created"),
            updated_at=data.get("dates").get("updated"),
            registrar=data.get("registrar"),
            registrant=data.get("registrant")
        )
