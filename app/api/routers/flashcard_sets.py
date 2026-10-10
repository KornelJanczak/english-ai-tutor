from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app.api.dependencies import get_example_sentence_generator, get_flashcard_set_service
from app.schemas.flashcard import FlashcardResponseSchema
from app.schemas.flashcard_set import (
    CreateFlashcardSetSchema,
    FlashcardSetResponseSchema,
    FlashcardSetWithFlashcardsResponseSchema,
    UpdateFlashcardSetSchema,
)
from app.services.ai_example_sentence_generator import AiExampleSentenceGenerator
from app.services.flashcard_set_service import FlashcardSetService

router = APIRouter(prefix="/flashcard-sets", tags=["flashcard-sets"])


@router.post(
    "",
    response_model=FlashcardSetWithFlashcardsResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_flashcard_set(
    data: CreateFlashcardSetSchema,
    service: FlashcardSetService = Depends(get_flashcard_set_service),
    ai_generator: AiExampleSentenceGenerator = Depends(get_example_sentence_generator),
) -> FlashcardSetWithFlashcardsResponseSchema:
     new_flashcard_set = await service.create_flashcard_set(data)
     await ai_generator.generate_example_sentences(new_flashcard_set.id)
     return new_flashcard_set


@router.get(
    "",
    response_model=list[FlashcardSetResponseSchema],
)
async def get_flashcard_sets(
    service: FlashcardSetService = Depends(get_flashcard_set_service),
) -> list[FlashcardSetResponseSchema]:
    return await service.get_flashcard_sets()


@router.get(
    "/{flashcard_set_id}",
    response_model=FlashcardSetResponseSchema,
)
async def get_flashcard_set(
    flashcard_set_id: str,
    service: FlashcardSetService = Depends(get_flashcard_set_service),
) -> FlashcardSetResponseSchema:
    flashcard_set = await service.get_flashcard_set(flashcard_set_id)
    if flashcard_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard set not found",
        )

    return flashcard_set


@router.get(
    "/{flashcard_set_id}/flashcards",
    response_model=list[FlashcardResponseSchema],
)
async def get_flashcards(
    flashcard_set_id: str,
    service: FlashcardSetService = Depends(get_flashcard_set_service),
) -> list[FlashcardResponseSchema]:
    flashcards = await service.get_flashcards(flashcard_set_id)
    if flashcards is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard set not found",
        )

    return flashcards


@router.patch(
    "/{flashcard_set_id}",
    response_model=FlashcardSetResponseSchema,
)
async def edit_flashcard_set(
    flashcard_set_id: str,
    data: UpdateFlashcardSetSchema,
    service: FlashcardSetService = Depends(get_flashcard_set_service),
) -> FlashcardSetResponseSchema:
    flashcard_set = await service.edit_flashcard_set(flashcard_set_id, data)
    if flashcard_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard set not found",
        )

    return flashcard_set


@router.delete(
    "/{flashcard_set_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_flashcard_set(
    flashcard_set_id: str,
    service: FlashcardSetService = Depends(get_flashcard_set_service),
) -> Response:
    deleted = await service.delete_flashcard_set(flashcard_set_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard set not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
