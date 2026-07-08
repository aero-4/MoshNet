from domains.infrastructure.services.safebrowsing import GoogleSafeBrowsing


class FakeClient:
    def __init__(self):
        self.request = None

    async def send_request(self, method: str, url: str, json: dict, params: dict):
        self.request = {
            "method": method,
            "url": url,
            "json": json,
            "params": params,
        }
        return {}


async def test_safe_browsing_sends_post_request():
    client = FakeClient()
    service = GoogleSafeBrowsing(client=client)

    data = await service.get_info("https://example.com", api_key="test-key")

    assert data == {
        "available": True,
        "safe": True,
        "matches": [],
    }
    assert client.request["method"] == "POST"
    assert client.request["params"] == {"key": "test-key"}
    assert client.request["json"]["client"]["clientId"] == "netmoshen"
    assert client.request["json"]["threatInfo"]["threatEntries"] == [
        {"url": "https://example.com"}
    ]
