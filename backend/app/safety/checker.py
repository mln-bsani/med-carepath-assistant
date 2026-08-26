from enum import Enum


class SafetyDecision(str, Enum):
    ALLOW = "allow"
    BLOCK_DIAGNOSIS = "block_diagnosis"
    BLOCK_PRESCRIPTION = "block_prescription"


def evaluate_intent(question: str) -> SafetyDecision:
    """
    Phase 1 intent-aware safety evaluator for M-CPA.

    This is a deterministic rule-based safety layer.

    It does NOT try to medically diagnose the user.
    It only classifies whether the user's request is within
    the allowed scope of M-CPA.
    """

    text = question.lower().strip()

    # --------------------------------------------------
    # ALLOWED HEALTHCARE / LAB CONTEXT
    # These patterns should NOT be blocked simply because
    # they contain medical terms.
    # --------------------------------------------------

    allowed_patterns = [
        "fasting",
        "fbs",
        "blood sugar",
        "test preparation",
        "sample",
        "specimen",
        "hematology",
        "hvs",
        "fbc",
        "laboratory",
        "lab",
        "unit",
        "department",
        "clinic",
        "test",
        "price",
        "kudi",
        "nawa ne",
        "ina",
        "a ina",
        "location",
        "workflow",
        "preparation",
        "shiri",
        "shirye-shirye",
        "sample",
        "samfur",
    ]

    # --------------------------------------------------
    # DIAGNOSIS INTENT
    # --------------------------------------------------

    diagnosis_patterns = [
        "wace cuta ce",
        "wane cuta ce",
        "me ke damuna",
        "me yake damuna",
        "ka tabbatar min",
        "ka gano min cuta",
        "diagnose me",
        "diagnosis",
        "what disease do i have",
        "what illness do i have",
        "confirm i have",
        "confirm that i have",
        "is it malaria",
    ]

    # --------------------------------------------------
    # PRESCRIPTION / DOSAGE INTENT
    # --------------------------------------------------

    prescription_patterns = [
        "wane magani zan sha",
        "wace magani zan sha",
        "wace magani zan yi anfani da shi",
        "rubuta min prescription",
        "rubuta min magani",
        "prescribe",
        "prescription",
        "what medicine should i take",
        "which medicine should i take",
        "what drug should i take",
        "dosage",
        "dose",
        "how many tablets should i take",
        "nawa zan sha",
    ]

    # --------------------------------------------------
    # INTENT DECISION
    # Restricted intents take priority.
    # --------------------------------------------------

    if any(pattern in text for pattern in prescription_patterns):
        return SafetyDecision.BLOCK_PRESCRIPTION

    if any(pattern in text for pattern in diagnosis_patterns):
        return SafetyDecision.BLOCK_DIAGNOSIS

    return SafetyDecision.ALLOW


def get_safety_message(decision: SafetyDecision) -> str:
    """
    Returns a user-friendly safety message.
    """

    if decision == SafetyDecision.BLOCK_DIAGNOSIS:
        return (
            "M-CPA ba ya iya tabbatar da cuta ko yin medical diagnosis. "
            "Domin samun cikakken bincike da diagnosis, da fatan za a tuntubi "
            "ƙwararren likita ko ma'aikacin lafiya."
        )

    if decision == SafetyDecision.BLOCK_PRESCRIPTION:
        return (
            "M-CPA ba ya rubuta prescription ko bayar da takamaiman magani "
            "ko dosage. Da fatan za a tuntubi ƙwararren likita ko pharmacist "
            "domin samun shawarar da ta dace."
        )

    return ""