from sqlalchemy.ext.asyncio import AsyncSession

from app.models.study_chat_error_analysis import StudyChatErrorAnalysis


class StudyChatErrorAnalysisRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        analysis: StudyChatErrorAnalysis,
    ) -> StudyChatErrorAnalysis:
        self.session.add(analysis)
        await self.session.flush()
        return analysis