from pydantic import BaseModel

#---------- Pydantic Schemas ----------
class NoteBase(BaseModel):
    title: str
    content: str | None = None

class NoteCreate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int
    class ConfigDict:
        orm_mode = True