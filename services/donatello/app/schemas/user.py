from pydantic import BaseModel


class UserCreationResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str = None
    last_name: str = None
    password: str


class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
