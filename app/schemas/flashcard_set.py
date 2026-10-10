from pydantic import BaseModel, ConfigDict, Field

from app.schemas.flashcard import (
    CreateFlashcardInSetSchema,
    FlashcardResponseSchema,
)


class CreateFlashcardSetSchema(BaseModel):
    name: str
    flashcards: list[CreateFlashcardInSetSchema]


class UpdateFlashcardSetSchema(BaseModel):
    name: str | None = None


class FlashcardSetResponseSchema(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class FlashcardSetWithFlashcardsResponseSchema(FlashcardSetResponseSchema):
    flashcards: list[FlashcardResponseSchema]
