from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="english-ai-tutor-api", version="0.1.0")

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
