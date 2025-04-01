from pydantic import BaseModel
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class RecipeBase(BaseModel):
    title: str
    description: str
    steps: str
    cooking_time: int
    image: Optional[str] = None
    categories: List[CategoryBase] = []

class RecipeResponse(RecipeBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[str] = None
    cooking_time: Optional[int] = None
    image: Optional[str] = None