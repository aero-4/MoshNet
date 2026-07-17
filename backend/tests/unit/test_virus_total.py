import httpx

from domains.infrastructure.services.virus_total import VirusTotalService


class FailingClient:
    def __init__(self):
        self.calls = 0

    async def send_request(self, method: str, url: str):
        self.calls += 1
        request = httpx.Request(method, url)
        response = httpx.Response(401, request=request)
        raise httpx.HTTPStatusError("Unauthorized", request=request, response=response)


class CountingClient:
    def __init__(self):
        self.calls = 0

    async def send_request(self, method: str, url: str):
        self.calls += 1
        return {}


async def test_virus_total_skips_request_without_api_key():
    client = CountingClient()
    service = VirusTotalService(client=client, api_key="")

    data = await service.get_info("example.com")

    assert client.calls == 0
    assert data.domain_org == "example.com"
    assert data.bad_statuses == []


async def test_virus_total_handles_unauthorized_response():
    client = FailingClient()
    service = VirusTotalService(client=client, api_key="bad-key")

    data = await service.get_info("example.com")

    assert client.calls == 1
    assert data.domain_org == "example.com"
    assert data.bad_statuses == []
