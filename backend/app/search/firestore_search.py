import re
from typing import Any, Optional

from app.core.firebase import get_firestore_client


# ---------------------------------------------------------
# QUERY NORMALIZATION
# ---------------------------------------------------------

def normalize_query(text: str) -> str:
    """
    Normalize text for deterministic comparison.

    Examples:
        "  INA   Hematology Unit yake? "
        -> "ina hematology unit yake"
    """

    text = text.lower().strip()

    # Remove punctuation while preserving letters and numbers.
    text = re.sub(r"[^\w\s]", " ", text)

    # Collapse multiple spaces.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------------------------------------
# KEYWORD EXTRACTION
# ---------------------------------------------------------

def extract_query_terms(question: str) -> list[str]:
    """
    Extract deterministic search terms from a user question.

    Phase 1 intentionally keeps this logic simple,
    transparent, and auditable.
    """

    normalized = normalize_query(question)

    # Common conversational words that are usually not useful
    # as medical knowledge search terms.
    stop_words = {
        "ina",
        "a",
        "ake",
        "ake yi",
        "shin",
        "me",
        "menene",
        "wane",
        "wace",
        "yake",
        "ce",
        "ne",
        "da",
        "na",
        "ka",
        "ta",
        "su",
        "the",
        "is",
        "are",
        "what",
        "where",
        "how",
        "does",
        "do",
        "i",
        "you",
        "before",
        "for",
        "and",
    }

    words = normalized.split()

    return [
        word
        for word in words
        if word not in stop_words and len(word) >= 2
    ]


# ---------------------------------------------------------
# DOCUMENT MATCHING
# ---------------------------------------------------------

def calculate_match_score(
    question: str,
    document: dict[str, Any],
) -> int:
    """
    Calculate a deterministic match score.

    Phase 1 scoring priority:

    1. Exact keyword phrase in question.
    2. Individual query terms found in keywords.
    3. Individual query terms found in tags.
    4. Individual query terms found in title.

    No AI or semantic inference is used here.
    """

    normalized_question = normalize_query(question)

    title = normalize_query(
        str(document.get("title", ""))
    )

    keywords = [
        normalize_query(str(keyword))
        for keyword in document.get("keywords", [])
    ]

    tags = [
        normalize_query(str(tag))
        for tag in document.get("tags", [])
    ]

    query_terms = extract_query_terms(question)

    score = 0

    # Highest confidence: exact multi-word keyword phrase.
    for keyword in keywords:
        if keyword and keyword in normalized_question:
            score += 10

    # Secondary matching: query terms against known fields.
    for term in query_terms:
        if term in keywords:
            score += 4

        if term in tags:
            score += 2

        if term and term in title:
            score += 1

    return score


# ---------------------------------------------------------
# FIRESTORE DETERMINISTIC SEARCH
# ---------------------------------------------------------

async def search_firestore(
    question: str,
) -> Optional[dict[str, Any]]:
    """
    Search M-CPA's verified Firestore knowledge base.

    Only documents that are:
        - verified == True
        - active == True

    are eligible to answer a user.
    """

    db = get_firestore_client()

    documents = (
        db.collection("knowledge_base")
        .where("verified", "==", True)
        .where("active", "==", True)
        .stream()
    )

    best_match: Optional[dict[str, Any]] = None
    best_score = 0

    for document_snapshot in documents:
        data = document_snapshot.to_dict()

        score = calculate_match_score(
            question=question,
            document=data,
        )

        if score > best_score:
            best_score = score

            best_match = {
                "id": document_snapshot.id,
                "score": score,
                **data,
            }

    return best_match