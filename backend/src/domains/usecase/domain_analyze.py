from domains.domain.entities import Domain


async def start_domain_analyze(domain: Domain, domain_dep):
    return await domain_dep.run(domain)
