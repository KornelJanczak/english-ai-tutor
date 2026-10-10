from uuid import uuid4

from app.models.flashcard import FlashCard
from app.models.flashcard_set import FlashcardSet
from app.repositories.flashcard_set_repository import FlashcardSetRepository
from app.schemas.flashcard_set import (
    CreateFlashcardSetSchema,
    UpdateFlashcardSetSchema,
)


class FlashcardSetService:
    def __init__(self, repository: FlashcardSetRepository):
        self.repository = repository

    async def create_flashcard_set(
        self,
        data: CreateFlashcardSetSchema,
    ) -> FlashcardSet:
        async with self.repository.session.begin():
            flashcard_set_id = str(uuid4())
            flashcard_set = FlashcardSet(
                id=flashcard_set_id,
                name=data.name,
            )
            flashcards = [
                FlashCard(
                    id=str(uuid4()),
                    definition=flashcard.definition,
                    definition_translation=flashcard.definition_translation,
                    ai_example_sentences=flashcard.example_sentences,
                    language=flashcard.language,
                    flashcard_set_id=flashcard_set_id,
                )
                for flashcard in data.flashcards
            ]
            flashcard_set.flashcards = flashcards

            return await self.repository.create_set_with_flashcards(
                flashcard_set,
                flashcards,
            )

    async def get_flashcard_set(
        self,
        flashcard_set_id: str,
    ) -> FlashcardSet | None:
        return await self.repository.get_flashcard_set_by_id(flashcard_set_id)

    async def get_flashcard_sets(self) -> list[FlashcardSet]:
        return await self.repository.get_flashcard_sets()

    async def edit_flashcard_set(
        self,
        flashcard_set_id: str,
        data: UpdateFlashcardSetSchema,
    ) -> FlashcardSet | None:
        async with self.repository.session.begin():
            flashcard_set = await self.repository.get_flashcard_set_by_id(
                flashcard_set_id
            )
            if flashcard_set is None:
                return None

            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(flashcard_set, field, value)

            await self.repository.session.flush()
            return flashcard_set

    async def delete_flashcard_set(self, flashcard_set_id: str) -> bool:
        async with self.repository.session.begin():
            flashcard_set = await self.repository.get_flashcard_set_by_id(
                flashcard_set_id
            )
            if flashcard_set is None:
                return False

            await self.repository.delete_flashcard_set(flashcard_set)
            return True

    async def get_flashcards(
        self,
        flashcard_set_id: str,
    ) -> list[FlashCard] | None:
        flashcard_set = await self.repository.get_flashcard_set_by_id(
            flashcard_set_id
        )
        if flashcard_set is None:
            return None

        return await self.repository.get_flashcards_by_set_id(flashcard_set_id)
