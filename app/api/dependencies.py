from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.flashcard_set_repository import FlashcardSetRepository
from app.repositories.study_chat_error_analysis_repository import (
    StudyChatErrorAnalysisRepository,
)
from app.services.flashcard_service import FlashcardService
from app.infrastructure.ai.client import create_ai_client
from app.infrastructure.ai.profiles import (
    ENGLISH_CHAT_PROFILE,
    FLASHCARD_EXAMPLES_PROFILE,
)
from app.infrastructure.ai.prompts import INLINE_INSPECTOR_PROMPT_VERSION
from app.services.ai_example_sentence_generator import (
    AiExampleSentenceGenerator,
)
from app.services.flashcard_set_service import FlashcardSetService
from app.services.study_chat_service import StudyChatService


def get_flashcard_repository(
    session: AsyncSession = Depends(get_db),
) -> FlashcardRepository:
    return FlashcardRepository(session)


def get_flashcard_set_repository(
    session: AsyncSession = Depends(get_db),
) -> FlashcardSetRepository:
    return FlashcardSetRepository(session)


def get_study_chat_error_analysis_repository(
    session: AsyncSession = Depends(get_db),
) -> StudyChatErrorAnalysisRepository:
    return StudyChatErrorAnalysisRepository(session)


def get_flashcard_service(
    repository: FlashcardRepository = Depends(get_flashcard_repository),
    flashcard_set_repository: FlashcardSetRepository = Depends(
        get_flashcard_set_repository
    ),
) -> FlashcardService:
    return FlashcardService(repository, flashcard_set_repository)


def get_flashcard_set_service(
    repository: FlashcardSetRepository = Depends(get_flashcard_set_repository),
) -> FlashcardSetService:
    return FlashcardSetService(repository)


def get_example_sentence_generator(
    flashcard_set_service: FlashcardSetService = Depends(
        get_flashcard_set_service
    ),
    flashcard_service: FlashcardService = Depends(get_flashcard_service),
) -> AiExampleSentenceGenerator:
    ai_client = create_ai_client(FLASHCARD_EXAMPLES_PROFILE)

    return AiExampleSentenceGenerator(ai_client, flashcard_set_service, flashcard_service)


def get_study_chat_service(
    flashcard_set_service: FlashcardSetService = Depends(
        get_flashcard_set_service
    ),
    error_analysis_repository: StudyChatErrorAnalysisRepository = Depends(
        get_study_chat_error_analysis_repository
    ),
) -> StudyChatService:
    ai_client = create_ai_client(ENGLISH_CHAT_PROFILE)
    return StudyChatService(
        ai_client,
        flashcard_set_service,
        error_analysis_repository,
        ENGLISH_CHAT_PROFILE.model,
        INLINE_INSPECTOR_PROMPT_VERSION,
    )
