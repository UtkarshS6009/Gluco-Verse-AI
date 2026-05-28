from pydantic import BaseModel

class SignupRequest(BaseModel):
    full_name: str
    email: str
    password: str
    role: str = "patient"

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    message: str
    user_id: int
    full_name: str
    email: str
    role: str
