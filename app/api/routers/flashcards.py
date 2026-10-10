from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app.api.dependencies import get_example_sentence_generator, get_flashcard_service
from app.schemas.ai import GeneratedExamplesSchema
from app.schemas.flashcard import (
    CreateFlashcardSchema,
    FlashcardResponseSchema,
    UpdateFlashcardSchema,
)
from app.services.ai_example_sentence_generator import AiExampleSentenceGenerator
from app.services.flashcard_service import FlashcardService

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.post("/{flashcard_set_id}/examples")
async def generate_example_sentences(
    flashcard_set_id: str,
    generator: AiExampleSentenceGenerator = Depends(
        get_example_sentence_generator
    ),
) -> list[GeneratedExamplesSchema]:
    example_sentences = await generator.generate_example_sentences(flashcard_set_id)

    if example_sentences is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard set not found",
        )

    return example_sentences


@router.post(
    "",
    response_model=FlashcardResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_flashcard(
    data: CreateFlashcardSchema,
    service: FlashcardService = Depends(get_flashcard_service),
) -> FlashcardResponseSchema:
    flashcard = await service.create_flashcard(data)
    if flashcard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard set not found",
        )

    return flashcard


@router.get(
    "/{flashcard_id}",
    response_model=FlashcardResponseSchema,
)
async def get_flashcard(
    flashcard_id: str,
    service: FlashcardService = Depends(get_flashcard_service),
) -> FlashcardResponseSchema:
    flashcard = await service.get_flashcard(flashcard_id)
    if flashcard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found",
        )

    return flashcard


@router.patch(
    "/{flashcard_id}",
    response_model=FlashcardResponseSchema,
)
async def edit_flashcard(
    flashcard_id: str,
    data: UpdateFlashcardSchema,
    service: FlashcardService = Depends(get_flashcard_service),
) -> FlashcardResponseSchema:
    flashcard = await service.edit_flashcard(flashcard_id, data)
    if flashcard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found",
        )

    return flashcard


@router.delete(
    "/{flashcard_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_flashcard(
    flashcard_id: str,
    service: FlashcardService = Depends(get_flashcard_service),
) -> Response:
    deleted = await service.delete_flashcard(flashcard_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
