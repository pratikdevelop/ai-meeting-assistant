from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.meetings import router as meetings_router
from backend.db.database import init_db
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Meeting Assistant API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-meeting-assistant",
    }


app.include_router(
    meetings_router,
)