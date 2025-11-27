
from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.routes import router as notes_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Notes API", version = "1.0")

origins = [
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",
    "http://localhost:8000",  # To serve frontend from backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables (models are imported above)
Base.metadata.create_all(bind=engine)

# include routes defined with APIRouter in app/api/routes.py
app.include_router(notes_router)

