from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypedDict

from app.models.flashcard import FlashCard

class FlashCardUpdateDict(TypedDict):
    id: str
    ai_example_sentences: list[str]


class FlashcardRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_flashcard(self, flashcard: FlashCard) -> FlashCard:
        self.session.add(flashcard)
        await self.session.flush()
        return flashcard

    async def update_example_sentences(self, updates: list[FlashCardUpdateDict]) -> None:
        await self.session.execute(update(FlashCard), updates)
        await self.session.flush()

    async def get_flashcard_by_id(self, flashcard_id: str) -> FlashCard | None:
        return await self.session.scalar(
            select(FlashCard).filter_by(id=flashcard_id)
        )

    async def edit_flashcard(self, flashcard: FlashCard) -> FlashCard:
        merged_flashcard = await self.session.merge(flashcard)
        await self.session.flush()
        return merged_flashcard

    async def delete_flashcard(self, flashcard: FlashCard) -> None:
        await self.session.delete(flashcard)
        await self.session.flush()
