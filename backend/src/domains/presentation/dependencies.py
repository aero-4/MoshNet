from fastapi import Depends

from domains.infrastructure.services.domain_analyze import DomainsAnalyze


def get_domain_analyzer():
    return DomainsAnalyze()


