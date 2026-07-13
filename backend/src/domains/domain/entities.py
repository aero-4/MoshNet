from urllib.parse import urlparse

from pydantic import BaseModel, Field, model_validator



class Domain(BaseModel):
    domain: str
    url: str | None = None

    @model_validator(mode="after")
    def normalize_domain_data(self):
        raw_value = self.domain.strip()
        if not raw_value:
            raise ValueError("Введите ссылку")

        url = raw_value if raw_value.startswith(("http://", "https://")) else f"https://{raw_value}"
        parsed = urlparse(url)
        if not parsed.hostname:
            raise ValueError("Ссылка имеет неправильный формат")

        self.url = url
        self.domain = parsed.hostname
        return self


class BadStatus(BaseModel):
    source: str
    category: str | None = None
    result: str | None = None


class DomainInfo(BaseModel):
    domain_org: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    registrar: dict | None = None
    registrant: dict | None = None
    last_analysis_stats: dict | None = None
    bad_statuses: list[BadStatus] = Field(default_factory=list)


class GoogleSafeBrowsingInfo(BaseModel):
    available: bool = False
    safe: bool = True
    matches: list = Field(default_factory=list)


class YandexSafeBrowsingInfo(BaseModel):
    available: bool = False
    safe: bool = True
    matches: list = Field(default_factory=list)


class SiteInfo(BaseModel):
    available: bool = True
    url: str
    error: str | None = None
    has_ssl: bool = False
    title: str | None = None
    description: str | None = None
    screenshot: str | None = None
    links: dict | None = None
    forms: dict | None = None
    suspicious_signals: list | None = None


class DomainAnalyzeInfo(BaseModel):
    risk_score: int = 0
    status: list[str] = []
    whois: DomainInfo | None = None
    virustotal: DomainInfo | None = None
    site: SiteInfo | None = None
    google_safebrowsing: GoogleSafeBrowsingInfo | None = None
    yandex_safebrowsing: YandexSafeBrowsingInfo | None = None
