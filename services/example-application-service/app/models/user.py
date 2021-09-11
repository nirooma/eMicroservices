from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=uuid.uuid4, primary_key=True)
    username: str
    password: str
    email: str

