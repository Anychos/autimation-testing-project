from tools.data_generator import fake_en
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(max_length=254, default_factory=fake_en.email)
    password: str = Field(min_length=8, max_length=64, default_factory=fake_en.password)


class RegisterResponseSchema(BaseModel):
    id: UUID
    email: EmailStr


class LoginRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=8, max_length=64)


class LoginResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
