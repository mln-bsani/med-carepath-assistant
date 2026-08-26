from typing import Literal, Optional

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    Request schema for questions sent to M-CPA.
    """

    question: str = Field(
        ...,
        min_length=2,
        max_length=500,
        description="User question for Med CarePath Assistant",
    )


class CPAResponse(BaseModel):
    """
    Strict Phase 1 response contract for M-CPA.

    Every response returned to the frontend must follow this structure.
    """

    status: Literal[
        "success",
        "not_found",
        "blocked",
        "needs_human",
    ]

    source: Literal[
        "firestore",
        "safety_guard",
        "system",
    ]

    answer: str

    verified: bool = False

    message: Optional[str] = None

    needs_human: bool = False