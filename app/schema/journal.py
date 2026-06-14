from pydantic import BaseModel


class JournalAnalysisRequest(BaseModel):
    content: str


class JournalAnalysisResponse(BaseModel):
    mood: str
    summary: str
    themes: list[str]
    suggestions: str
