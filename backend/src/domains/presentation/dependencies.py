from redis.asyncio import Redis

from core.settings import settings
from domains.infrastructure.services.domain_analyze import DomainsAnalyze


def get_domain_analyzer():
    return DomainsAnalyze()


def get_redis_client():
    redis = Redis.from_url(url=settings.REDIS_URI)
    return redis
