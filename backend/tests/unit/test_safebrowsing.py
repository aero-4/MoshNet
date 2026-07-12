from domains.infrastructure.services.google_safebrowsing import GoogleSafeBrowsing
from domains.infrastructure.services.yandex_safebrowsing import YandexSafeBrowsing


class FakeClient:
    def __init__(self, response: dict | None = None):
        self.request = None
        self.response = response or {}

    async def send_request(self, method: str, url: str, json: dict, params: dict):
        self.request = {
            "method": method,
            "url": url,
            "json": json,
            "params": params,
        }
        return self.response


async def test_safe_browsing_sends_post_request():
    client = FakeClient()
    service = GoogleSafeBrowsing(client=client)

    data = await service.get_info("https://example.com", api_key="test-key")

    assert data.available is True
    assert data.safe is True
    assert data.matches == []
    assert client.request["method"] == "POST"
    assert client.request["params"] == {"key": "test-key"}
    assert client.request["json"]["client"]["clientId"] == "netmoshen"
    assert client.request["json"]["threatInfo"]["threatEntries"] == [
        {"url": "https://example.com"}
    ]


async def test_yandex_safe_browsing_handles_empty_response():
    client = FakeClient()
    service = YandexSafeBrowsing(client=client)

    data = await service.get_info("https://example.com", api_key="test-key")

    assert data.available is True
    assert data.safe is True
    assert data.matches == []
    assert client.request["method"] == "POST"
    assert client.request["url"] == YandexSafeBrowsing.BASE_URL
    assert client.request["params"] == {"key": "test-key"}
    assert client.request["json"]["client"]["clientId"] == "netmoshen"
    assert client.request["json"]["threatInfo"]["threatEntries"] == [
        {"url": "https://example.com"}
    ]


async def test_yandex_safe_browsing_marks_matches_unsafe():
    match = {"threatType": "MALWARE", "threat": {"url": "https://bad.test"}}
    client = FakeClient({"matches": [match]})
    service = YandexSafeBrowsing(client=client)

    data = await service.get_info("https://bad.test", api_key="test-key")

    assert data.available is True
    assert data.safe is False
    assert data.matches == [match]


async def test_yandex_safe_browsing_normalizes_domain_to_url():
    client = FakeClient()
    service = YandexSafeBrowsing(client=client)

    await service.get_info("example.com", api_key="test-key")

    assert client.request["json"]["threatInfo"]["threatEntries"] == [
        {"url": "https://example.com"}
    ]
