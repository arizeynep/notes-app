from app.db.models import Note
from app.db.database import get_db
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.domain.note import NoteCreate, NoteOut

# create a router so we can register routes on the app from main.py
router = APIRouter()

# ---------- Routes ----------
@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/notes", response_model=List[NoteOut])
def list_notes(db: Session = Depends(get_db)):
    return db.query(Note).order_by(Note.created_at.desc()).all()

@router.post("/notes", response_model=NoteOut, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code = 404, detail="Note not found")
    return note

@router.put("/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note_data: NoteCreate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code = 404, detail="Note not found")
    note.title = note_data.title
    note.content = note_data.content
    db.commit()
    db.refresh(note)
    return note

@router.delete("/notes/{note_id}", status_code = 204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code = 404, detail="Note not found")
    db.delete(note)
    db.commit()
    return None
