from fastapi import FastAPI

from app.api.routers.flashcard_sets import router as flashcard_sets_router
from app.api.routers.flashcards import router as flashcards_router
from app.api.routers.study_chat import router as study_chat_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="english-ai-tutor-api",
        version="0.1.0",
    )
    app.include_router(flashcards_router)
    app.include_router(flashcard_sets_router)
    app.include_router(study_chat_router)

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
