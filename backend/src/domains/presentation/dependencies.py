from fastapi import Depends
from redis.asyncio import Redis

from core.settings import settings
from domains.infrastructure.services.domain_analyze import DomainsAnalyze


def get_domain_analyzer():
    return DomainsAnalyze()


def get_redis_client():
    return Redis.from_url(url=settings.REDIS_URI)