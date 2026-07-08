import pytest

from domains.infrastructure.services.safebrowsing import GoogleSafeBrowsing
from domains.infrastructure.services.site_parser import SiteParser
from domains.infrastructure.services.virus_total import VirusTotalService
from domains.infrastructure.services.whois import WhoDatAsService


@pytest.mark.parametrize(
    "domain", ["google.com", "yandex.ru", "nvidia.com"]
)
async def test_check_domain_who_dat(domain):
    service = WhoDatAsService()
    data = await service.get_info(domain=domain)
    assert data.domain_org == domain


@pytest.mark.parametrize(
    "domain", ["google.com", "yandex.ru", "nvidia.com"]
)
async def test_check_domain_virus_total(domain):
    service = VirusTotalService()
    data = await service.get_info(domain=domain)
    assert data.domain_org == domain
    assert data.last_analysis_stats is not None


async def test_check_domain_virus_total_bad_statuses():
    domain = "www.xv-ru.com"
    service = VirusTotalService()
    data = await service.get_info(domain=domain)

    assert data.domain_org == domain
    assert data.bad_statuses
    assert any(
        status.category in service.BAD_CATEGORIES
        or str(status.result).lower() in service.BAD_RESULTS
        for status in data.bad_statuses
    )


async def test_check_domain_site_parser():
    url = "https://www.xv-ru.com/"
    service = SiteParser()
    data = await service.get_info(url)

    assert data.get("url") == url
    assert data.get("available") == True


async def test_check_domain_google_safe_browsing():
    url = "https://www.xv-ru.com"
    service = GoogleSafeBrowsing()
    data = await service.get_info(url)
