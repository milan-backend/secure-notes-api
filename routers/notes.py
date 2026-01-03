from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select
from database import engine
from models import Note
from models import User
from routers.auth import get_current_user
from schemas import NoteCreate

router = APIRouter(prefix="/notes",tags=["notes"])


#  CREATE NOTES

@router.post("/")
def create_notes(
    note:NoteCreate,
    current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        new_note = Note(
            title = note.title,
            content = note.content,
            user_id = current_user.id
        )

        session.add(new_note)
        session.commit()
        session.refresh(new_note)
        
        return new_note


# GET THE NOTES

@router.get("/")
def get_my_notes(
    current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        notes = session.exec(select(Note).where(Note.user_id==current_user.id)).all()
        return notes
    

#  DELETE NOTES

@router.delete("/{note_id}")
def delete_my_note(
    note_id :int,
    current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        note = session.get(Note,note_id)

        if not note:
            raise HTTPException(status_code=404,detail="Note not found.")
        
        if note.user_id != current_user.id:
            raise HTTPException(status_code=403,detail="Not Allowed.")
        
        session.delete(note)
        session.commit()

        return {"message":"Note Deleted."}