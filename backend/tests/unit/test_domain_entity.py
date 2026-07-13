from domains.domain.entities import Domain


def test_domain_keeps_original_url_and_extracts_hostname():
    domain = Domain(domain="http://example.com/catalog/item?from=test")

    assert domain.url == "http://example.com/catalog/item?from=test"
    assert domain.domain == "example.com"


def test_domain_adds_https_only_when_scheme_is_missing():
    domain = Domain(domain="example.com/catalog/item")

    assert domain.url == "https://example.com/catalog/item"
    assert domain.domain == "example.com"
