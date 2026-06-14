from fastapi import APIRouter, Depends

from app.api.dependencies import get_journal_service
from app.schema.journal import JournalAnalysisRequest, JournalAnalysisResponse
from app.services.journal_service import JournalService

journal_router = APIRouter(prefix="/journal", tags=["journal"])


@journal_router.post("/analyze", response_model=JournalAnalysisResponse)
def analyze_journal(
    request: JournalAnalysisRequest,
    journal_service: JournalService = Depends(get_journal_service),
) -> JournalAnalysisResponse:
    return journal_service.analyze(request)
