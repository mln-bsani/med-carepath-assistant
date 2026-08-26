from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai.schemas import QuestionRequest, CPAResponse
from app.ai.service import process_question

from app.core.firebase import get_firestore_client


app = FastAPI(
    title="Med CarePath Assistant API",
    description="Backend API for M-CPA healthcare navigation and workflow assistance.",
    version="0.1.0",
)


# ---------------------------------------------------------
# CORS CONFIGURATION
# ---------------------------------------------------------

allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/")
async def root():
    return {
        "message": "Med CarePath Assistant API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "M-CPA API"
    }

@app.get("/firebase-test")
async def firebase_test():
    """
    Temporary endpoint to test the backend connection to Firestore.
    """

    try:
        db = get_firestore_client()

        # Simple Firestore operation
        collections = list(db.collections())

        return {
            "status": "connected",
            "message": "Firebase Admin successfully connected to Firestore.",
            "collections_found": len(collections),
        }

    except Exception as error:
        return {
            "status": "error",
            "message": str(error),
        }
# ---------------------------------------------------------
# PHASE 1 - AI QUERY ENDPOINT
# ---------------------------------------------------------

@app.post(
    "/api/v1/ai/query",
    response_model=CPAResponse,
)
async def query_ai(request: QuestionRequest):
    """
    Main Phase 1 entry point for M-CPA questions.

    Current flow:
    QuestionRequest
        ↓
    Pydantic Validation
        ↓
    Service Layer
        ↓
    CPAResponse
    """

    return await process_question(request)