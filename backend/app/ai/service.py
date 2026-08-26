from app.ai.schemas import QuestionRequest, CPAResponse
from app.safety.checker import (
    SafetyDecision,
    evaluate_intent,
    get_safety_message,
)
from app.search.firestore_search import search_firestore


async def process_question(request: QuestionRequest) -> CPAResponse:
    """
    Main Phase 1 orchestration layer for M-CPA.

    Current flow:

    Validated Question
            ↓
    Safety Intent Evaluation
            ↓
       Allowed?
       ↙      ↘
     YES      NO
      ↓        ↓
    Firestore   Blocked Response
      ↓
    Found?
    ↙    ↘
  YES     NO
   ↓       ↓
SUCCESS  NOT_FOUND
   ↓
Verified Response
    """

    question = request.question.strip()

    # --------------------------------------------------
    # STEP 1: SAFETY / INTENT EVALUATION
    # --------------------------------------------------

    safety_decision = evaluate_intent(question)

    if safety_decision != SafetyDecision.ALLOW:
        return CPAResponse(
            status="blocked",
            source="safety_guard",
            answer=get_safety_message(safety_decision),
            verified=False,
            message="Request restricted by M-CPA safety policy.",
            needs_human=True,
        )

    # --------------------------------------------------
    # STEP 2: DETERMINISTIC FIRESTORE SEARCH
    # --------------------------------------------------

    search_result = await search_firestore(question)

    # --------------------------------------------------
    # STEP 3: VERIFIED INFORMATION FOUND
    # --------------------------------------------------

    if search_result is not None:
        return CPAResponse(
            status="success",
            source="firestore",
            answer=search_result.get(
                "content",
                "An sami bayanin da ya dace."
            ),
            verified=True,
            message=search_result.get("title"),
            needs_human=False,
        )

    # --------------------------------------------------
    # STEP 4: VERIFIED INFORMATION NOT FOUND
    # --------------------------------------------------

    return CPAResponse(
        status="not_found",
        source="system",
        answer=(
            "Ba a sami ingantaccen bayani game da wannan tambayar "
            "a cikin tsarin M-CPA ba."
        ),
        verified=False,
        message=(
            "The requested information was not found in the "
            "verified knowledge base."
        ),
        needs_human=False,
    )