from app.ai.schemas import QuestionRequest, CPAResponse
from app.safety.checker import (
    SafetyDecision,
    evaluate_intent,
    get_safety_message,
)


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
    Search    Blocked Response
      ↓
    Not Found / Success
    """

    question = request.question.strip()

    # --------------------------------------------------
    # STEP 1: SAFETY / INTENT EVALUATION
    # --------------------------------------------------

    safety_decision = evaluate_intent(question)

    # --------------------------------------------------
    # STEP 2: BLOCK RESTRICTED INTENTS IMMEDIATELY
    # --------------------------------------------------

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
    # STEP 3: DETERMINISTIC SEARCH PLACEHOLDER
    # Firestore will be connected in the next step.
    # --------------------------------------------------

    return CPAResponse(
        status="not_found",
        source="system",
        answer=(
            "Ba a sami ingantaccen bayani game da wannan tambayar "
            "a cikin tsarin M-CPA ba."
        ),
        verified=False,
        message="The requested information was not found in the verified system.",
        needs_human=False,
    )