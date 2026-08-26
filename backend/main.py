from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai.schemas import QuestionRequest, CPAResponse
from app.ai.service import process_question


app = FastAPI(
    title="Med CarePath Assistant API",
    description=(
        "Backend API for healthcare navigation, laboratory workflow, "
        "and verified healthcare information assistance."
    ),
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
# API STATUS
# ---------------------------------------------------------

@app.get("/")
async def root():
    return {
        "message": "Med CarePath Assistant API is running"
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "M-CPA API",
        "version": "0.1.0",
    }


# ---------------------------------------------------------
# MAIN M-CPA QUERY ENDPOINT
# ---------------------------------------------------------

@app.post(
    "/api/v1/ai/query",
    response_model=CPAResponse,
)
async def query_ai(request: QuestionRequest) -> CPAResponse:
    """
    Main M-CPA query endpoint.

    Flow:
    1. Input validation
    2. Intent-aware safety evaluation
    3. Deterministic Firestore search
    4. Structured response
    """

    return await process_question(request)