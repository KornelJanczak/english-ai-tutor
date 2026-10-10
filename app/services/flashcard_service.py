from uuid import uuid4

from app.models.flashcard import FlashCard
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.flashcard_set_repository import FlashcardSetRepository
from app.schemas.flashcard import (
    CreateFlashcardSchema,
    UpdateFlashcardSchema,
)
from app.repositories.flashcard_repository import FlashCardUpdateDict


class FlashcardService:
    def __init__(
        self,
        repository: FlashcardRepository,
        flashcard_set_repository: FlashcardSetRepository,
    ):
        self.repository = repository
        self.flashcard_set_repository = flashcard_set_repository

    async def create_flashcard(
        self,
        data: CreateFlashcardSchema,
    ) -> FlashCard | None:
        async with self.repository.session.begin():
            flashcard_set = await self.flashcard_set_repository.get_flashcard_set_by_id(
                data.flashcard_set_id
            )
            if flashcard_set is None:
                return None

            flashcard = FlashCard(
                id=str(uuid4()),
                definition=data.definition,
                definition_translation=data.definition_translation,
                ai_example_sentences=data.example_sentences,
                language=data.language,
                flashcard_set_id=data.flashcard_set_id,
            )

            return await self.repository.create_flashcard(flashcard)

    async def update_flashcards(self, updates: list[FlashCardUpdateDict]) -> None:
        async with self.repository.session.begin():
            await self.repository.update_example_sentences(updates)

    async def get_flashcard(self, flashcard_id: str) -> FlashCard | None:
        return await self.repository.get_flashcard_by_id(flashcard_id)

    async def edit_flashcard(
        self,
        flashcard_id: str,
        data: UpdateFlashcardSchema,
    ) -> FlashCard | None:
        async with self.repository.session.begin():
            flashcard = await self.repository.get_flashcard_by_id(flashcard_id)
            if flashcard is None:
                return None

            updates = data.model_dump(exclude_unset=True)
            for field, value in updates.items():
                setattr(flashcard, field, value)

            await self.repository.session.flush()
            return flashcard

    async def delete_flashcard(self, flashcard_id: str) -> bool:
        async with self.repository.session.begin():
            flashcard = await self.repository.get_flashcard_by_id(flashcard_id)
            if flashcard is None:
                return False

            await self.repository.delete_flashcard(flashcard)
            return True
