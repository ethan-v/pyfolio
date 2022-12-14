from typing import Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    slug: Optional[str] = None
    image: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = False
    created_at: Optional[str]
    updated_at: Optional[str]


class PostCreate(PostBase):
    category_id: int


class PostUpdate(PostBase):
    title: Optional[str]
    slug: Optional[str]
    image: Optional[str]
    excerpt: Optional[str]
    content: Optional[str]
    category_id: Optional[int]
    is_active: Optional[bool]


class PostResponse(PostBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True
