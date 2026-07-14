import json

from redis.asyncio import Redis

from domains.domain.entities import Domain
from domains.infrastructure.services.domain_analyze import DomainsAnalyze


async def start_domain_analyze(domain: Domain, domain_dep: DomainsAnalyze, redis: Redis):
    value = await redis.get(domain.domain)
    if value:
        return json.loads(value)

    result = await domain_dep.run(domain)
    await redis.set(domain.domain,
                    json.dumps(result.model_dump(mode="json")),
                    ex=10000)
    return result
