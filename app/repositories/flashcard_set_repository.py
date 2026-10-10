from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.flashcard import FlashCard
from app.models.flashcard_set import FlashcardSet


class FlashcardSetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_flashcard_set(
        self,
        flashcard_set: FlashcardSet,
    ) -> FlashcardSet:
        self.session.add(flashcard_set)
        await self.session.flush()
        return flashcard_set


    async def get_flashcard_set_by_id(
        self,
        flashcard_set_id: str,
    ) -> FlashcardSet | None:
        return await self.session.scalar(
            select(FlashcardSet)
            .options(selectinload(FlashcardSet.flashcards))
            .filter_by(id=flashcard_set_id)
        )

    async def get_flashcard_sets(self) -> list[FlashcardSet]:
        result = await self.session.scalars(select(FlashcardSet))
        return result.all()

    async def create_set_with_flashcards(
        self,
        flashcard_set: FlashcardSet,
        flashcards: list[FlashCard],
    ) -> FlashcardSet:
        self.session.add(flashcard_set)
        self.session.add_all(flashcards)

        await self.session.flush()
        return flashcard_set

    async def edit_flashcard_set(self, flashcard_set: FlashcardSet) -> FlashcardSet:
        merged_flashcard_set = await self.session.merge(flashcard_set)
        await self.session.flush()
        return merged_flashcard_set

    async def delete_flashcard_set(self, flashcard_set: FlashcardSet) -> None:
        await self.session.delete(flashcard_set)
        await self.session.flush()

    async def get_flashcards_by_set_id(
        self,
        flashcard_set_id: str,
    ) -> list[FlashCard]:
        result = await self.session.scalars(
            select(FlashCard).filter_by(
                flashcard_set_id=flashcard_set_id
            )
        )

        return result.all()
