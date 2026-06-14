import json

from openai import OpenAI

from app.core.config import settings
from app.schema.journal import JournalAnalysisRequest, JournalAnalysisResponse

SYSTEM_PROMPT = """\
You are a thoughtful journaling assistant. Analyze the provided journal entry and respond ONLY with a JSON object using this exact structure:
{
  "mood": "<single word or short phrase describing overall mood>",
  "summary": "<2-3 sentence summary of the entry>",
  "themes": ["<theme1>", "<theme2>", "..."],
  "suggestions": "<one actionable suggestion based on the entry>"
}"""


class JournalService:
    def __init__(self) -> None:
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def analyze(self, request: JournalAnalysisRequest) -> JournalAnalysisResponse:
        response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.content},
            ],
            response_format={"type": "json_object"},
            temperature=0.4,
        )

        raw = response.choices[0].message.content or "{}"
        data = json.loads(raw)
        return JournalAnalysisResponse(**data)
