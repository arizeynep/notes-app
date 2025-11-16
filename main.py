
from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.routes import router as notes_router

app = FastAPI(title="Notes API", version = "1.0")

# create tables (models are imported above)
Base.metadata.create_all(bind=engine)

# include routes defined with APIRouter in app/api/routes.py
app.include_router(notes_router)

