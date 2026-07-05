from fastapi import APIRouter, Depends

from domains.domain.entities import Domain
from domains.presentation.dependencies import DomainAnalyzeDep, get_domain_analyzer
from domains.usecase.domain_analyze import start_domain_analyze

router = APIRouter()


@router.post("/analyze/")
async def start_analyze_domain(domain_data: Domain, domain_dep=Depends(get_domain_analyzer)):
    return await start_domain_analyze(domain_data, domain_dep)
