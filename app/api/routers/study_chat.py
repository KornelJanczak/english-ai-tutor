from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from langchain_core.messages import AIMessage, HumanMessage

from app.api.dependencies import get_study_chat_service
from app.schemas.chat import StudyChatMessageSchema, StudyChatResponseSchema
from app.services.study_chat_service import StudyChatService

router = APIRouter(prefix="/study-chat", tags=["study-chat"])


@router.post(
    "/{flashcard_set_id}/message",
    response_model=StudyChatResponseSchema,
)
async def study_chat_message(
    flashcard_set_id: str,
    data: StudyChatMessageSchema,
    service: StudyChatService = Depends(get_study_chat_service),
) -> StudyChatResponseSchema:
    response_parts = []

    async for chunk in service.stream_reply(
        flashcard_set_id,
        data.message,
        [],
        data.language_level,
    ):
        response_parts.append(chunk)

    return StudyChatResponseSchema(
        response="".join(response_parts),
        inline_inspector=await service.inspect_message(
            flashcard_set_id,
            data.message,
            data.language_level,
        ),
    )


@router.websocket("/{flashcard_set_id}")
async def study_chat(
    websocket: WebSocket,
    flashcard_set_id: str,
    service: StudyChatService = Depends(get_study_chat_service),
) -> None:
    await websocket.accept()
    history = []

    try:
        while True:
            data = StudyChatMessageSchema.model_validate(await websocket.receive_json())
            response_parts = []

            async for token in service.stream_reply(
                flashcard_set_id,
                data.message,
                history,
                data.language_level,
            ):
                response_parts.append(token)
                await websocket.send_json({"type": "token", "content": token})

            response = "".join(response_parts)
            history.extend(
                [HumanMessage(content=data.message),
                 AIMessage(content=response)]
            )

            inline_inspector = await service.inspect_message(
                flashcard_set_id,
                data.message,
                data.language_level,
            )
            await websocket.send_json(
                {
                    "type": "done",
                    "inline_inspector": inline_inspector.model_dump(),
                }
            )
    except LookupError as error:
        await websocket.send_json({"type": "error", "detail": str(error)})
        await websocket.close(code=4404)
    except WebSocketDisconnect:
        return
