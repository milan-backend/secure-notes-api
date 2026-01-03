from pydantic import BaseModel

# FOR SIGNUP REQUEST

class SignupRequest(BaseModel):
    name :str
    email :str
    password :str


# FOR LOGIN REQUEST

class LoginRequest(BaseModel):
    email :str
    password :str


# CREATE NOTES REQUEST

class NoteCreate(BaseModel):
    title :str
    content :str

