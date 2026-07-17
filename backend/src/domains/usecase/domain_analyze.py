import json

from redis.asyncio import Redis

from domains.domain.entities import Domain
from domains.infrastructure.services.domain_analyze import DomainsAnalyze



async def start_domain_analyze(domain: Domain, domain_dep: DomainsAnalyze, redis: Redis):
    try:
        value = await redis.get(domain.url)
        if value:
            return json.loads(value)
    except:
        pass

    result = await domain_dep.run(domain)
    try:
        await redis.set(domain.url,
                        json.dumps(result.model_dump(mode="json")),
                        ex=1000)
    except:
        pass
    return result
