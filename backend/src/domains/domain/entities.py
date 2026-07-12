import datetime
import re
from typing import Any

import pydantic
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

from domains.domain.interfaces.service import ServiceI


class Domain(BaseModel):
    domain: str

    @field_validator("domain", mode="after")
    @classmethod
    def validate_domain_format(cls, v: str) -> str:
        url_pattern = re.compile(
            r"^(https?://)?"
            r"(www\.)?"
            r"(?P<domain>([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,6})"
            r"(/[a-zA-Z0-9\.\&\/\?\:@\-_=#%~]*)*$"
        )

        match = url_pattern.match(v.strip())

        if not match:
            raise HTTPException(
                status_code=403, detail="Ссылка имеет неправильный формат"
            )

        clean_domain = match.group("domain")

        return clean_domain


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


class DomainAnalyzeInfo(BaseModel):
    risk_score: int = 0
    whois: DomainInfo
    virustotal: DomainInfo
    site: dict
    google_safebrowsing: GoogleSafeBrowsingInfo
    yandex_safebrowsing: YandexSafeBrowsingInfo
