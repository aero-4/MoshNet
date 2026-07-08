import datetime
import re
from typing import Any

import pydantic
from fastapi import HTTPException
from pydantic import BaseModel, Field

from domains.domain.interfaces.service import ServiceI


class Domain(BaseModel):
    domain: str

    @pydantic.field_validator("domain", mode="after")
    def validate_domain_format(cls, v: Any):
        url_pattern = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
        if not re.search(url_pattern, v):
            raise HTTPException(status_code=403, detail="Ссылка имеет неправильный формат")

        return v


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


class DomainAnalyze(BaseModel):
    risk_score: int = 0
    whois: DomainInfo
    virustotal:  DomainInfo
    site: dict
    safebrowsing: dict
