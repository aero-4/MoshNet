import json

from redis.asyncio import Redis

from domains.domain.entities import Domain
from domains.infrastructure.services.domain_analyze import DomainsAnalyze


async def start_domain_analyze(
    domain: Domain, domain_dep: DomainsAnalyze, redis: Redis
):
    if redis:
        value = await redis.get(domain.url)
        if value:
            return json.loads(value)

    result = await domain_dep.run(domain)
    if redis:
        await redis.set(domain.url, json.dumps(result.model_dump(mode="json")), ex=1000)

    return result
