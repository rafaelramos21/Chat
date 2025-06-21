from pydantic import BaseModel
from datetime import datetime

class AlbumCreate(BaseModel):
    user_id: str
    name: str

class AlbumOut(BaseModel):
    id: int
    user_id: str
    name: str
    created_at: datetime

    class Config:
        orm_mode = True

class PhotoCreate(BaseModel):
    album_id: int
    file_url: str

class PhotoOut(BaseModel):
    id: int
    album_id: int
    file_url: str
    created_at: datetime

    class Config:
        orm_mode = True
