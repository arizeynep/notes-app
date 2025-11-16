
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Note

from pydantic import BaseModel
from typing import List, Optional

Base.metadata.create_all(bind = engine)
app = FastAPI(title="Notes API", version = "1.0")

# Dependency: create a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Pydantic Schemas ----------
class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int
    class Config:
        orm_mode = True

# ---------- Routes ----------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/notes", response_model=List[NoteOut])
def list_notes(db: Session = Depends(get_db)):
    return db.query(Note).order_by(Note.created_at.desc()).all()

@app.post("/notes", response_model=NoteOut, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code = 404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note_data: NoteCreate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code = 404, detail="Note not found")
    note.title = note_data.title
    note.content = note_data.content
    db.commit()
    db.refresh(note)
    return note

@app.delete("/notes/{note_id}", status_code = 204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code = 404, detail="Note not found")
    db.delete(note)
    db.commit()
    return None
