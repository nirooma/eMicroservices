from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(primary_key=True)
    is_active: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.utcnow())
    is_staff: bool = Field(default=False, description="Admin Panel Access")
    is_superuser: bool = Field(default=False, description="All Permissions By Default")
    first_name: Optional[str] = Field(nullable=True)
    last_name: Optional[str] = Field(nullable=True)
    password: str = Field(description="Hashed Password")
    username: str

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id})>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
