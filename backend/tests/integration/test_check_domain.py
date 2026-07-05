import pytest

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
    service = VirusTotalService()
    data = await service.get_info(domain="www.xv-ru.com")

    assert data.domain_org == "www.xv-ru.com"
    assert data.bad_statuses
    assert any(
        status.category in service.BAD_CATEGORIES
        or str(status.result).lower() in service.BAD_RESULTS
        for status in data.bad_statuses
    )

