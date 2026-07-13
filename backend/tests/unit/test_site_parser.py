from domains.infrastructure.services.site_parser import SiteParser


class FakeClient:
    async def send_request(self, method: str, url: str, return_json: bool = True):
        assert method == "GET"
        assert url == "https://example.com"
        assert return_json is False

        return """
        <html>
            <head>
                <title>Example shop</title>
                <meta name="description" content="Safe demo page">
            </head>
            <body>
                <a href="/catalog">Catalog</a>
                <a href="https://blog.example.com/post">Blog</a>
                <a href="https://payments.example-pay.test/checkout">Pay</a>
                <a href="#section">Skip</a>
                <form action="https://payments.example-pay.test/login">
                    <input type="password" name="password">
                </form>
            </body>
        </html>
        """


class FakePathClient:
    async def send_request(self, method: str, url: str, return_json: bool = True):
        assert method == "GET"
        assert url == "http://example.com/catalog/item"
        assert return_json is False

        return """
        <html>
            <head>
                <title>Product page</title>
            </head>
            <body></body>
        </html>
        """


async def test_site_parser_extracts_page_signals():
    service = SiteParser(client=FakeClient())
    service._make_screenshot = lambda url: None

    data = await service.get_info("example.com")

    assert data["available"] is True
    assert data["url"] == "https://example.com"
    assert data["title"] == "Example shop"
    assert data["description"] == "Safe demo page"
    assert data["links"]["total"] == 3
    assert data["links"]["internal"] == 2
    assert data["links"]["external"] == 1
    assert data["forms"]["total"] == 1
    assert data["forms"]["password_fields"] == 1
    assert data["forms"]["external_actions"] == [
        "https://payments.example-pay.test/login"
    ]
    assert data["suspicious_signals"] == [
        "password_input",
        "external_form_action",
    ]


async def test_site_parser_keeps_original_url_with_scheme_and_path():
    service = SiteParser(client=FakePathClient())
    service._make_screenshot = lambda url: None

    data = await service.get_info("http://example.com/catalog/item")

    assert data["available"] is True
    assert data["url"] == "http://example.com/catalog/item"
    assert data["has_ssl"] is False
    assert data["title"] == "Product page"
