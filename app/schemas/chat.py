from pydantic import BaseModel, Field
from enum import StrEnum


class LanguageErrorType(StrEnum):
    GRAMMAR = "grammar"
    VOCABULARY = "vocabulary"
    SPELLING = "spelling"
    WORD_ORDER = "word_order"
    COLLOCATION = "collocation"
    NATURALNESS = "naturalness"
    PUNCTUATION = "punctuation"


class LanguageError(BaseModel):
    original_fragment: str
    corrected_fragment: str
    error_type: LanguageErrorType
    explanation: str
    start_index: int | None = None
    end_index: int | None = None


class InlineInspectorSchema(BaseModel):
    original_message: str
    corrected_message: str | None = None
    errors: list[LanguageError] = Field(default_factory=list)


class StudyChatResponseSchema(BaseModel):
    response: str
    inline_inspector: InlineInspectorSchema


class StudyChatMessageSchema(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    language_level: str = Field(default="B2", max_length=20)
